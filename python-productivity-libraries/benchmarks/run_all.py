"""
Run all benchmarks and generate a summary report.
"""

import subprocess
import sys
from pathlib import Path


def run_benchmark(script_name):
    """Run a single benchmark script."""
    print(f"\n{'='*80}")
    print(f"Running: {script_name}")
    print(f"{'='*80}\n")
    
    script_path = Path(__file__).parent / script_name
    
    try:
        result = subprocess.run(
            [sys.executable, str(script_path)],
            capture_output=False,
            text=True,
            check=True
        )
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Benchmark failed: {script_name}")
        return False


def main():
    """Run all available benchmarks."""
    print("="*80)
    print(" "*20 + "PYTHON PRODUCTIVITY LIBRARIES")
    print(" "*25 + "BENCHMARK SUITE")
    print("="*80)
    
    benchmarks = [
        'flashtext_benchmark.py',
        'ujson_benchmark.py',
    ]
    
    results = {}
    
    for benchmark in benchmarks:
        success = run_benchmark(benchmark)
        results[benchmark] = success
    
    # Summary
    print(f"\n{'='*80}")
    print("BENCHMARK SUMMARY")
    print(f"{'='*80}")
    
    for benchmark, success in results.items():
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{status:12} {benchmark}")
    
    total = len(results)
    passed = sum(1 for s in results.values() if s)
    
    print(f"\nResults: {passed}/{total} benchmarks passed")
    print(f"{'='*80}")
    
    if passed == total:
        print("\n🎉 All benchmarks completed successfully!")
        return 0
    else:
        print("\n⚠️  Some benchmarks failed. Check output above.")
        return 1


if __name__ == '__main__':
    sys.exit(main())
