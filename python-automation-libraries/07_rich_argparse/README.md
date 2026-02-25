# 07 — Rich-Argparse: Beautiful CLI Help Pages

One import. One `formatter_class`. Your argparse `--help` output
becomes color-coded, syntax-highlighted, and scannable.

## Run the Example

```bash
python cli_runner.py --help
python cli_runner.py --env dev --dry-run
python cli_runner.py --env prod --source api_v2 --limit 500
```

## Key Concepts

- Import `RichHelpFormatter` from `rich_argparse`
- Set `formatter_class=RichHelpFormatter` in `ArgumentParser`
- Zero changes to argument definitions — drop-in replacement
- Colors, bold, and layout handled automatically via Rich
