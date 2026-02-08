# Quick Start Guide

Get up and running with Python JIT benchmarks in 5 minutes.

## Prerequisites

You need both Python 3.14 and Python 3.15 installed. We recommend using `pyenv`:

```bash
# Install pyenv (if not already installed)
curl https://pyenv.run | bash

# Install Python versions
pyenv install 3.14.0
pyenv install 3.15.0a3  # or latest alpha/beta release

# Verify installations
python3.14 --version
python3.15 --version
```

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/python-jit-etl-benchmark.git
cd python-jit-etl-benchmark

# Install dependencies (optional, for visualization)
pip install -r requirements.txt
```

## Run Your First Benchmark

### Step 1: Generate Test Data

```bash
python benchmarks/generate_data.py
```

This creates `data/transactions_input.csv` with 100,000 transaction records.

### Step 2: Benchmark Python 3.14 (Baseline)

```bash
python3.14 benchmarks/run_benchmark.py
```

You'll see output like:
```
Run 1/5:
  Time: 47.32s
  Valid: 80,042 | Invalid: 19,958
  Throughput: 2,113 records/sec
...
Average time: 47.35s (±0.15s)
```

### Step 3: Benchmark Python 3.15 with JIT

```bash
PYTHON_JIT=1 python3.15 benchmarks/run_benchmark.py
```

Expected output:
```
Run 1/5:
  Time: 43.82s
  Valid: 80,042 | Invalid: 19,958
  Throughput: 2,283 records/sec
...
Average time: 43.83s (±0.12s)
```

### Step 4: Compare Results Automatically

```bash
python benchmarks/compare_versions.py
```

This will:
- Run benchmarks on both versions
- Calculate improvement percentage
- Show ROI calculation
- Save results to `results/performance_comparison.json`

## Understanding the Results

A typical successful benchmark shows:

- **7-8% improvement** on ARM (M-series Mac)
- **4-6% improvement** on x86-64 (Intel/AMD)
- **Consistent results** across runs (low std dev)
- **Higher throughput** with JIT enabled

## Troubleshooting

### "Python 3.15 not found"
Make sure you've installed Python 3.15 and it's in your PATH:
```bash
pyenv global 3.15.0a3
which python3.15
```

### "JIT not enabled"
Check if your Python 3.15 build includes JIT:
```bash
python3.15 -c "import sys; print(hasattr(sys, '_jit'))"
```

Should return `True`. If not, reinstall Python 3.15 with JIT support.

### "No such file: transactions_input.csv"
Run the data generation script first:
```bash
python benchmarks/generate_data.py
```

## Next Steps

- **Read the full results**: Check `results/benchmark_results.json`
- **Test on your data**: Modify `src/transaction_processor.py` for your ETL logic
- **Share your results**: Open an issue or PR with your findings
- **Read the article**: [Link to Medium article]

## Quick Reference

```bash
# Generate data
python benchmarks/generate_data.py

# Benchmark Python 3.14
python3.14 benchmarks/run_benchmark.py

# Benchmark Python 3.15 + JIT
PYTHON_JIT=1 python3.15 benchmarks/run_benchmark.py

# Automated comparison
python benchmarks/compare_versions.py

# Run with your own data
python3.15 src/transaction_processor.py --input your_data.csv --output results.csv
```

Happy benchmarking! 🚀
