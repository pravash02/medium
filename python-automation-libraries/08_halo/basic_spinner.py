"""
08_halo/basic_spinner.py  +  pipeline_with_spinner.py
-------------------------------------------------------
Halo: terminal spinners for long-running automation tasks.
Gives scripts the UX polish of a proper application.
"""

import time
import random
from halo import Halo


# ═══════════════════════════════════════════════════════
# PART 1: Basic Spinner Patterns
# ═══════════════════════════════════════════════════════

def demo_basic_patterns():
    print("=" * 55)
    print("HALO  Basic Spinner Patterns")
    print("=" * 55)
    print()

    #  1. Context manager (auto-stops on exit) ─
    print("1. Context manager pattern (auto-stop):\n")
    with Halo(text="Loading configuration...", spinner="dots"):
        time.sleep(1.2)
    # Spinner disappears  for success, use .succeed() instead

    #  2. Success state 
    print("2. Explicit states:\n")

    spinner = Halo(text="Connecting to database...", spinner="dots")
    spinner.start()
    time.sleep(1.0)
    spinner.succeed("Connected to database")

    spinner = Halo(text="Validating API credentials...", spinner="dots")
    spinner.start()
    time.sleep(0.8)
    spinner.succeed("API credentials valid")

    #  3. Failure state 
    spinner = Halo(text="Fetching remote config...", spinner="dots")
    spinner.start()
    time.sleep(0.9)
    spinner.fail("Remote config unavailable  using local fallback")

    #  4. Warning state 
    spinner = Halo(text="Checking rate limits...", spinner="arc")
    spinner.start()
    time.sleep(0.7)
    spinner.warn("Approaching rate limit  throttling enabled")

    #  5. Info state ─
    spinner = Halo(text="Scanning for pending jobs...", spinner="arc")
    spinner.start()
    time.sleep(0.8)
    spinner.info("Found 42 pending jobs in queue")

    #  6. Dynamic text update 
    print("\n3. Dynamic text update:\n")
    spinner = Halo(text="Fetching page 1...", spinner="dots2")
    spinner.start()
    for page in range(1, 5):
        spinner.text = f"Fetching page {page} of 4..."
        time.sleep(0.5)
    spinner.succeed(f"Fetched 4 pages successfully")

    print()


# ═══════════════════════════════════════════════════════
# PART 2: Full Automation Pipeline with Spinners
# ═══════════════════════════════════════════════════════

def simulate_work(duration: float, fail_rate: float = 0.0) -> bool:
    """Simulates async work. Returns False if it 'fails'."""
    time.sleep(duration)
    return random.random() > fail_rate


def run_pipeline_stage(
    name: str,
    duration: float,
    spinner_style: str = "dots",
    fail_rate: float = 0.0,
) -> bool:
    """Runs a single pipeline stage with a Halo spinner."""
    spinner = Halo(text=name, spinner=spinner_style)
    spinner.start()
    success = simulate_work(duration, fail_rate)
    if success:
        spinner.succeed(f"{name}  done")
    else:
        spinner.fail(f"{name}  FAILED")
    return success


def demo_pipeline_with_spinners():
    print("=" * 55)
    print("HALO  Full Automation Pipeline")
    print("=" * 55)
    print()

    pipeline_stages = [
        # (stage name,                   duration, spinner,      fail_rate)
        ("Initializing pipeline",         0.6,      "dots",       0.0),
        ("Loading source credentials",    0.8,      "arc",        0.0),
        ("Connecting to data source",     1.1,      "dots2",      0.0),
        ("Fetching records (batch 1/3)",  1.2,      "dots",       0.0),
        ("Fetching records (batch 2/3)",  1.0,      "dots",       0.0),
        ("Fetching records (batch 3/3)",  0.9,      "dots",       0.0),
        ("Validating schema",             0.7,      "arc",        0.0),
        ("Applying transformations",      1.3,      "dots2",      0.0),
        ("Writing to output",             0.8,      "dots",       0.0),
        ("Sending completion webhook",    0.5,      "arc",        0.0),
    ]

    start_time = time.perf_counter()
    passed = 0
    failed = 0

    for stage_name, duration, spinner_type, fail_rate in pipeline_stages:
        success = run_pipeline_stage(stage_name, duration, spinner_type, fail_rate)
        if success:
            passed += 1
        else:
            failed += 1

    elapsed = time.perf_counter() - start_time
    print()

    # Final summary (using Halo one-liner)
    if failed == 0:
        with Halo(text="", spinner="dots") as h:
            h.succeed(
                f"Pipeline complete  {passed} stages passed, "
                f"0 failed  {elapsed:.1f}s total"
            )
    else:
        with Halo(text="", spinner="dots") as h:
            h.fail(f"Pipeline finished with {failed} failure(s)  check logs above")


# ═══════════════════════════════════════════════════════
# PART 3: try/except Pattern (production-ready)
# ═══════════════════════════════════════════════════════

def demo_try_except_pattern():
    print("\n" + "=" * 55)
    print("HALO  Try/Except Pattern (production-ready)")
    print("=" * 55)
    print()

    operations = [
        ("Syncing CRM records", 0.8, False),
        ("Uploading to S3",     0.7, True),   # This one will "fail"
        ("Sending alerts",      0.5, False),
    ]

    for op_name, duration, should_fail in operations:
        spinner = Halo(text=op_name, spinner="dots")
        spinner.start()
        try:
            time.sleep(duration)
            if should_fail:
                raise ConnectionError("S3 endpoint unreachable (timeout)")
            spinner.succeed(op_name)
        except Exception as e:
            spinner.fail(f"{op_name}  {e}")
            # In production: log error, send alert, continue or break


#  Main

if __name__ == "__main__":
    demo_basic_patterns()
    demo_pipeline_with_spinners()
    demo_try_except_pattern()
    print()
