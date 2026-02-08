"""
Automated benchmark comparison between Python versions.

Compares Python 3.14 (no JIT) vs Python 3.15 (with JIT).
"""

import subprocess
import sys
import json
from pathlib import Path
from typing import Dict, List


def check_python_version(python_cmd: str) -> Dict:
    """Check Python version and JIT availability."""
    try:
        result = subprocess.run(
            [python_cmd, '--version'],
            capture_output=True,
            text=True,
            check=True
        )
        version = result.stdout.strip()
        
        # Check JIT support
        jit_check = subprocess.run(
            [python_cmd, '-c', 
             'import sys; print(hasattr(sys, "_jit") and hasattr(sys._jit, "is_enabled"))'],
            capture_output=True,
            text=True
        )
        has_jit = jit_check.stdout.strip() == 'True'
        
        return {
            'command': python_cmd,
            'version': version,
            'has_jit': has_jit
        }
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def run_benchmark_for_version(python_cmd: str, enable_jit: bool, runs: int) -> Dict:
    """Run benchmark for specific Python version."""
    env = {}
    if enable_jit:
        env['PYTHON_JIT'] = '1'
    
    jit_label = "WITH JIT" if enable_jit else "NO JIT"
    print(f"\n{'='*60}")
    print(f"Running benchmark: {python_cmd} ({jit_label})")
    print(f"{'='*60}")
    
    result_file = f"results/benchmark_{python_cmd.replace('.', '_')}_{jit_label.replace(' ', '_')}.json"
    
    cmd = [
        python_cmd,
        'benchmarks/run_benchmark.py',
        '--runs', str(runs),
        '--save-results', result_file
    ]
    
    # Update environment
    import os
    run_env = os.environ.copy()
    run_env.update(env)
    
    try:
        subprocess.run(cmd, env=run_env, check=True)
        
        # Load and return results
        with open(result_file, 'r') as f:
            return json.load(f)
    except subprocess.CalledProcessError as e:
        print(f"Error running benchmark: {e}")
        return None
    except FileNotFoundError as e:
        print(f"Result file not found: {e}")
        return None


def compare_results(baseline: Dict, comparison: Dict) -> Dict:
    """Compare two benchmark results."""
    baseline_time = baseline['statistics']['mean']
    comparison_time = comparison['statistics']['mean']
    
    improvement = ((baseline_time - comparison_time) / baseline_time) * 100
    speedup = baseline_time / comparison_time
    time_saved = baseline_time - comparison_time
    
    return {
        'baseline_time': baseline_time,
        'comparison_time': comparison_time,
        'improvement_percent': improvement,
        'speedup_factor': speedup,
        'time_saved_seconds': time_saved,
        'baseline_throughput': baseline['statistics']['avg_throughput'],
        'comparison_throughput': comparison['statistics']['avg_throughput']
    }


def print_comparison(baseline_name: str, comparison_name: str, comparison: Dict):
    """Print formatted comparison results."""
    print("\n" + "="*60)
    print("PERFORMANCE COMPARISON")
    print("="*60)
    print(f"Baseline: {baseline_name}")
    print(f"Comparison: {comparison_name}")
    print("-"*60)
    
    improvement = comparison['improvement_percent']
    if improvement > 0:
        print(f"✓ IMPROVEMENT: {improvement:.1f}% faster")
        print(f"  Speedup: {comparison['speedup_factor']:.2f}x")
        print(f"  Time saved: {comparison['time_saved_seconds']:.2f}s per run")
    elif improvement < 0:
        print(f"✗ REGRESSION: {abs(improvement):.1f}% slower")
    else:
        print("= NO CHANGE")
    
    print("-"*60)
    print(f"Baseline time: {comparison['baseline_time']:.2f}s")
    print(f"Comparison time: {comparison['comparison_time']:.2f}s")
    print(f"Baseline throughput: {comparison['baseline_throughput']:,.0f} rec/sec")
    print(f"Comparison throughput: {comparison['comparison_throughput']:,.0f} rec/sec")
    print("="*60)


def calculate_roi(time_saved_per_run: float, runs_per_day: int = 156):
    """Calculate ROI based on daily pipeline runs."""
    daily_savings = time_saved_per_run * runs_per_day
    monthly_savings = daily_savings * 30
    annual_savings = daily_savings * 365
    
    print("\n" + "="*60)
    print("ROI CALCULATION")
    print("="*60)
    print(f"Assuming {runs_per_day} pipeline runs per day:")
    print(f"  Daily savings: {daily_savings/60:.1f} minutes")
    print(f"  Monthly savings: {monthly_savings/3600:.1f} hours")
    print(f"  Annual savings: {annual_savings/3600:.1f} hours")
    print("="*60)


def main():
    """Main comparison script."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Compare Python versions')
    parser.add_argument('--python314', default='python3.14',
                       help='Python 3.14 command (default: python3.14)')
    parser.add_argument('--python315', default='python3.15',
                       help='Python 3.15 command (default: python3.15)')
    parser.add_argument('--runs', type=int, default=5,
                       help='Number of benchmark runs per version (default: 5)')
    parser.add_argument('--skip-generate', action='store_true',
                       help='Skip data generation (use existing data)')
    
    args = parser.parse_args()
    
    # Check Python versions
    print("Checking Python versions...")
    py314 = check_python_version(args.python314)
    py315 = check_python_version(args.python315)
    
    if not py314:
        print(f"Error: Python 3.14 not found ({args.python314})")
        sys.exit(1)
    
    if not py315:
        print(f"Error: Python 3.15 not found ({args.python315})")
        sys.exit(1)
    
    print(f"✓ Found: {py314['version']}")
    print(f"✓ Found: {py315['version']}")
    
    if not py315['has_jit']:
        print("Warning: Python 3.15 doesn't have JIT support")
    
    # Create results directory
    Path('results').mkdir(exist_ok=True)
    
    # Generate data if needed
    if not args.skip_generate:
        print("\nGenerating test data...")
        subprocess.run([sys.executable, 'benchmarks/generate_data.py'], check=True)
    
    # Run benchmarks
    results_314 = run_benchmark_for_version(args.python314, False, args.runs)
    results_315_jit = run_benchmark_for_version(args.python315, True, args.runs)
    
    if not results_314 or not results_315_jit:
        print("Error: Benchmark failed")
        sys.exit(1)
    
    # Compare results
    comparison = compare_results(results_314, results_315_jit)
    
    # Print comparison
    print_comparison(
        f"{args.python314} (no JIT)",
        f"{args.python315} (with JIT)",
        comparison
    )
    
    # Calculate ROI
    calculate_roi(comparison['time_saved_seconds'])
    
    # Save comparison
    comparison_file = 'results/performance_comparison.json'
    with open(comparison_file, 'w') as f:
        json.dump({
            'baseline': results_314,
            'comparison': results_315_jit,
            'analysis': comparison
        }, f, indent=2)
    
    print(f"\n✓ Comparison saved to {comparison_file}")


if __name__ == '__main__':
    main()
