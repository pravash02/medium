"""
07_rich_argparse/cli_runner.py
--------------------------------
A realistic automation pipeline CLI using Rich-Argparse.
Run with --help to see the beautifully formatted output.

Usage:
  python cli_runner.py --help
  python cli_runner.py --env dev --dry-run
  python cli_runner.py --env prod --source api_v2 --limit 500 --output ./reports
"""

import argparse
import sys
from rich_argparse import RichHelpFormatter
from rich.console import Console
from rich.table import Table
from rich import print as rprint

console = Console()


#  Argument Parser 

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="automation-pipeline",
        description=(
            "[bold]Python Automation Pipeline Runner[/bold]\n\n"
            "Fetches data from configured sources, applies transformations, "
            "and loads results to the target destination. "
            "Supports dry-run mode for safe testing."
        ),
        epilog=(
            "Examples:\n"
            "  %(prog)s --env dev --dry-run\n"
            "  %(prog)s --env prod --source api_v2 --limit 1000\n"
            "  %(prog)s --env prod --source csv --output ./reports --verbose"
        ),
        formatter_class=RichHelpFormatter,  # ← The only change needed!
    )

    #  Environment 
    env_group = parser.add_argument_group("Environment")
    env_group.add_argument(
        "--env",
        choices=["dev", "staging", "prod"],
        default="dev",
        metavar="ENV",
        help="Target environment. Choices: [bold]dev[/bold], staging, prod. (default: dev)",
    )
    env_group.add_argument(
        "--config",
        type=str,
        default="./config.json",
        metavar="PATH",
        help="Path to config file. (default: ./config.json)",
    )

    #  Data Source 
    source_group = parser.add_argument_group("Data Source")
    source_group.add_argument(
        "--source",
        choices=["api_v1", "api_v2", "csv", "airtable", "webhook"],
        default="api_v2",
        metavar="SOURCE",
        help="Input data source. (default: api_v2)",
    )
    source_group.add_argument(
        "--limit",
        type=int,
        default=100,
        metavar="N",
        help="Maximum number of records to process per run. (default: 100)",
    )
    source_group.add_argument(
        "--since",
        type=str,
        metavar="DATE",
        help="Only process records created after this date (ISO 8601, e.g. 2026-01-01).",
    )

    #  Output 
    output_group = parser.add_argument_group("Output")
    output_group.add_argument(
        "--output",
        type=str,
        default="./output",
        metavar="DIR",
        help="Directory for output files. (default: ./output)",
    )
    output_group.add_argument(
        "--format",
        choices=["json", "csv", "parquet"],
        default="json",
        metavar="FMT",
        help="Output file format. (default: json)",
    )

    #  Behavior flags 
    flags_group = parser.add_argument_group("Behavior Flags")
    flags_group.add_argument(
        "--dry-run",
        action="store_true",
        help="Simulate pipeline execution without writing any output.",
    )
    flags_group.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging with per-record detail.",
    )
    flags_group.add_argument(
        "--fail-fast",
        action="store_true",
        help="Stop on first error instead of continuing and reporting at end.",
    )

    return parser


#  Pipeline simulation 

def run_pipeline(args: argparse.Namespace):
    """Simulates pipeline execution based on parsed args."""

    # Print config summary as a Rich table
    table = Table(title="Pipeline Configuration", show_header=True, header_style="bold cyan")
    table.add_column("Setting",  style="dim", width=20)
    table.add_column("Value",    style="bold")

    rows = [
        ("Environment",   args.env),
        ("Source",        args.source),
        ("Record Limit",  str(args.limit)),
        ("Output Dir",    args.output),
        ("Output Format", args.format),
        ("Since",         args.since or "all time"),
        ("Dry Run",       "Yes — no writes" if args.dry_run else "No"),
        ("Verbose",       "Yes" if args.verbose else "No"),
        ("Fail Fast",     "Yes" if args.fail_fast else "No"),
    ]
    for setting, value in rows:
        table.add_row(setting, value)

    console.print()
    console.print(table)
    console.print()

    if args.dry_run:
        rprint("[bold yellow]⚠ DRY RUN MODE — No data will be written.[/bold yellow]\n")

    # Simulate stages
    stages = [
        f"Connecting to [bold]{args.source}[/bold] source...",
        f"Fetching up to [bold]{args.limit}[/bold] records...",
        "Applying transformations...",
        f"Validating output schema ([bold]{args.format}[/bold])...",
    ]

    if not args.dry_run:
        stages.append(f"Writing results to [bold]{args.output}/[/bold]...")

    for stage in stages:
        rprint(f"  ✓ {stage}")

    console.print()
    rprint(f"[bold green]Pipeline complete![/bold green] "
           f"Processed [bold]{min(args.limit, 42)}[/bold] records in 1.23s.")


#  Entry point 

def main():
    parser = build_parser()

    # Show help if no args given
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)

    args = parser.parse_args()

    # Validation
    if args.env == "prod" and args.dry_run is False and args.limit > 10_000:
        parser.error("Production runs are capped at 10,000 records. Use --limit ≤ 10000.")

    run_pipeline(args)


if __name__ == "__main__":
    main()
