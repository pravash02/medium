"""
03_pyfilesystem2/backend_swap.py  &  testing_with_memfs.py
------------------------------------------------------------
Shows the key superpower of PyFilesystem2: the same business logic
runs against any backend. Swap local → memory → S3 with one line.
"""

from fs import open_fs
from fs.base import FS
import json


#  Business logic — completely storage-agnostic 

def process_reports(filesystem: FS, output_dir: str = "output") -> dict:
    """
    Reads all .json files from 'input/' in the given filesystem,
    aggregates values, writes a summary to 'output/summary.json'.

    This function doesn't know or care what backend it's running against.
    """
    filesystem.makedirs("input", recreate=True)
    filesystem.makedirs(output_dir, recreate=True)

    # Seed some input data (in real use, data would already be there)
    records = [
        {"region": "north", "sales": 42_000},
        {"region": "south", "sales": 38_500},
        {"region": "east",  "sales": 61_200},
    ]
    for r in records:
        filesystem.writetext(f"input/{r['region']}.json", json.dumps(r))

    # Process
    total_sales = 0
    regions_processed = []
    for filename in filesystem.listdir("input"):
        if filename.endswith(".json"):
            data = json.loads(filesystem.readtext(f"input/{filename}"))
            total_sales += data["sales"]
            regions_processed.append(data["region"])

    summary = {
        "total_sales": total_sales,
        "regions": regions_processed,
        "avg_sales": total_sales / len(regions_processed),
    }

    filesystem.writetext(
        f"{output_dir}/summary.json",
        json.dumps(summary, indent=2)
    )
    return summary


#  Backend Swap Demo ─

def demo_backend_swap():
    print("=" * 55)
    print("PYFILESYSTEM2 — Backend Swap Demo")
    print("=" * 55)

    #  Local filesystem 
    print("\n Backend: Local OS Filesystem \n")
    import os, shutil
    os.makedirs("./fs_swap_demo", exist_ok=True)
    with open_fs("osfs://./fs_swap_demo") as local_fs:
        result = process_reports(local_fs)
        print(f"  Summary: {result}")
    shutil.rmtree("./fs_swap_demo")

    #  In-memory filesystem (no disk I/O) 
    print("\n Backend: In-Memory Filesystem \n")
    with open_fs("mem://") as mem_fs:
        result = process_reports(mem_fs)
        print(f"  Summary: {result}")
        # Verify it's really in memory (no files on disk)
        print(f"  Files in memory: {list(mem_fs.walk.files())}")

    #  S3 (commented out — requires fs-s3fs and AWS credentials) ─
    # print("\n Backend: Amazon S3 \n")
    # with open_fs("s3://my-automation-bucket") as s3_fs:
    #     result = process_reports(s3_fs, output_dir="reports/output")
    #     print(f"  Summary written to S3: {result}")

    print("\n Same process_reports() function ran on both backends unchanged.")


#  Unit Testing with MemoryFilesystem ─

def demo_testing_with_memfs():
    """
    Demonstrates using mem:// as a test double — no temp files,
    no cleanup, fully isolated, blazing fast.
    """
    print("\n" + "=" * 55)
    print("PYFILESYSTEM2 — Testing with MemoryFilesystem")
    print("=" * 55)

    tests_passed = 0

    # Test 1: Summary is calculated correctly
    print("\n Test 1: Correct aggregation ")
    with open_fs("mem://") as mem_fs:
        summary = process_reports(mem_fs)
        assert summary["total_sales"] == 141_700, "Total sales mismatch!"
        assert len(summary["regions"]) == 3, "Should have 3 regions!"
        assert "summary.json" in mem_fs.listdir("output"), "summary.json missing!"
        print("  PASS — totals and output file correct")
        tests_passed += 1

    # Test 2: Average is correct
    print("\n Test 2: Average calculation ")
    with open_fs("mem://") as mem_fs:
        summary = process_reports(mem_fs)
        expected_avg = 141_700 / 3
        assert abs(summary["avg_sales"] - expected_avg) < 0.01, "Average mismatch!"
        print(f"  PASS — avg_sales = {summary['avg_sales']:,.2f}")
        tests_passed += 1

    # Test 3: Custom output directory
    print("\n Test 3: Custom output directory ")
    with open_fs("mem://") as mem_fs:
        process_reports(mem_fs, output_dir="custom_output")
        assert mem_fs.isdir("custom_output"), "Custom dir not created!"
        assert mem_fs.isfile("custom_output/summary.json"), "File not in custom dir!"
        print("  PASS — custom output directory created correctly")
        tests_passed += 1

    print(f"\n {tests_passed}/3 tests passed — zero temp files created on disk.")


if __name__ == "__main__":
    demo_backend_swap()
    demo_testing_with_memfs()
