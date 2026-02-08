"""
Benchmark runner for transaction processor.

Runs multiple iterations and collects timing statistics.
"""

import sys
import time
import json
import statistics
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from transaction_processor import process_batch


def run_benchmark(input_file: str, output_file: str, num_runs: int = 5) -> dict:
    """
    Run benchmark multiple times and collect statistics.
    
    Args:
        input_file: Path to input CSV
        output_file: Path to output CSV
        num_runs: Number of benchmark runs
        
    Returns:
        Dictionary with benchmark results
    """
    print(f"Running benchmark: {num_runs} iterations")
    print(f"Python version: {sys.version}")
    
    # Check JIT status
    jit_enabled = False
    if hasattr(sys, '_jit') and hasattr(sys._jit, 'is_enabled'):
        jit_enabled = sys._jit.is_enabled()
    
    print(f"JIT enabled: {jit_enabled}")
    print("-" * 60)
    
    run_times = []
    valid_counts = []
    invalid_counts = []
    
    for run_num in range(1, num_runs + 1):
        print(f"\nRun {run_num}/{num_runs}:")
        
        start = time.perf_counter()
        valid, invalid, elapsed = process_batch(input_file, output_file, verbose=False)
        end = time.perf_counter()
        
        runtime = end - start
        run_times.append(runtime)
        valid_counts.append(valid)
        invalid_counts.append(invalid)
        
        total = valid + invalid
        throughput = total / runtime
        
        print(f"  Time: {runtime:.2f}s")
        print(f"  Valid: {valid:,} | Invalid: {invalid:,}")
        print(f"  Throughput: {throughput:,.0f} records/sec")
    
    # Calculate statistics
    avg_time = statistics.mean(run_times)
    std_dev = statistics.stdev(run_times) if len(run_times) > 1 else 0
    min_time = min(run_times)
    max_time = max(run_times)
    
    total_records = valid_counts[0] + invalid_counts[0]
    avg_throughput = total_records / avg_time
    
    results = {
        'timestamp': datetime.now().isoformat(),
        'python_version': sys.version,
        'jit_enabled': jit_enabled,
        'num_runs': num_runs,
        'total_records': total_records,
        'run_times': run_times,
        'statistics': {
            'mean': avg_time,
            'std_dev': std_dev,
            'min': min_time,
            'max': max_time,
            'avg_throughput': avg_throughput
        }
    }
    
    # Print summary
    print("\n" + "=" * 60)
    print("BENCHMARK RESULTS")
    print("=" * 60)
    print(f"Python: {sys.version.split()[0]}")
    print(f"JIT: {'ENABLED' if jit_enabled else 'DISABLED'}")
    print(f"Records: {total_records:,}")
    print(f"Runs: {num_runs}")
    print("-" * 60)
    print(f"Average time: {avg_time:.2f}s (±{std_dev:.2f}s)")
    print(f"Min time: {min_time:.2f}s")
    print(f"Max time: {max_time:.2f}s")
    print(f"Avg throughput: {avg_throughput:,.0f} records/sec")
    print("=" * 60)
    
    return results


def save_results(results: dict, output_file: str):
    """Save benchmark results to JSON file."""
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\n✓ Results saved to {output_file}")


def main():
    """Main benchmark runner."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Run transaction processor benchmark')
    parser.add_argument('--input', default='data/transactions_input.csv',
                       help='Input CSV file')
    parser.add_argument('--output', default='data/transactions_output.csv',
                       help='Output CSV file')
    parser.add_argument('--runs', type=int, default=5,
                       help='Number of benchmark runs (default: 5)')
    parser.add_argument('--save-results', default='results/benchmark_results.json',
                       help='Path to save results JSON')
    
    args = parser.parse_args()
    
    # Create results directory if it doesn't exist
    Path(args.save_results).parent.mkdir(parents=True, exist_ok=True)
    
    # Run benchmark
    results = run_benchmark(args.input, args.output, args.runs)
    
    # Save results
    save_results(results, args.save_results)


if __name__ == '__main__':
    main()
