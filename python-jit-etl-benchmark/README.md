# Python JIT ETL Benchmark

> Real-world benchmarks of Python 3.15's JIT compiler on ETL workloads

[![Python 3.14+](https://img.shields.io/badge/python-3.14%2B-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## 📊 Overview

This repository contains reproducible benchmarks testing Python 3.15's experimental JIT compiler on realistic ETL (Extract, Transform, Load) workloads. 

**Key Finding:** Python 3.15 with JIT enabled shows **7.4% performance improvement** on pure-Python ETL validation and transformation logic.

## 🎯 What This Tests

- **Transaction validation pipeline** processing 100,000 records
- **47 business rules** in pure Python (currency validation, amount checks, date parsing, risk scoring)
- **Real-world ETL patterns**: CSV processing, data enrichment, string manipulation
- **ARM64 (M-series Mac)** and **x86-64 Linux** architectures

## 🚀 Quick Start

### Prerequisites

```bash
# Install Python 3.14 and 3.15
pyenv install 3.14.0
pyenv install 3.15.0a3  # or latest alpha/beta

# Clone the repository
git clone https://github.com/yourusername/python-jit-etl-benchmark.git
cd python-jit-etl-benchmark

# Install dependencies
pip install -r requirements.txt
```

### Run Benchmarks

```bash
# Generate sample data
python benchmarks/generate_data.py

# Run benchmark (Python 3.14 - no JIT)
python3.14 benchmarks/run_benchmark.py

# Run benchmark (Python 3.15 - with JIT)
PYTHON_JIT=1 python3.15 benchmarks/run_benchmark.py

# Run automated comparison
python benchmarks/compare_versions.py
```

## 📈 Results

### MacBook Pro M2 (ARM64)

| Python Version | Average Time | Improvement | Records/sec |
|---------------|--------------|-------------|-------------|
| 3.14.0 (baseline) | 47.35s | - | 2,112 |
| 3.15.0a3 (JIT) | 43.83s | **7.4% faster** | 2,281 |

**Savings per run:** 3.52 seconds  
**Daily savings (156 runs):** 9.2 minutes  
**Annual savings:** 55.7 hours

### x86-64 Linux (Expected)

| Python Version | Average Time | Improvement |
|---------------|--------------|-------------|
| 3.14.0 | ~50s | - |
| 3.15.0a3 (JIT) | ~47s | ~6% faster |

*Note: x86-64 shows slightly lower gains than ARM64 (consistent with official benchmarks)*

## 🔬 What We Learned

### ✅ Where JIT Helps

- **Pure-Python validation logic** (7-15% faster)
- **String manipulation and formatting** (5-10% faster)
- **Loop-heavy transformations** (10-20% faster)
- **Dictionary operations** (5-8% faster)

### ❌ Where JIT Doesn't Help

- **NumPy/Pandas operations** (0% improvement)
- **I/O-bound code** (CSV reading/writing - 0% improvement)
- **C-extension libraries** (already optimized)
- **Short-running scripts** (cold-start overhead negates gains)

### ⚠️ Gotchas

- **First run slower** (~5% due to compilation overhead)
- **Not compatible with free-threaded Python** (no-GIL builds)
- **Minimal benefit for Pandas-heavy workflows**

## 📁 Repository Structure

```
python-jit-etl-benchmark/
├── src/
│   ├── transaction_processor.py   # Main ETL pipeline
│   ├── validators.py               # Validation logic (47 rules)
│   └── enrichers.py                # Data enrichment functions
├── benchmarks/
│   ├── generate_data.py            # Creates test datasets
│   ├── run_benchmark.py            # Single benchmark runner
│   └── compare_versions.py         # Automated comparison script
├── data/
│   ├── transactions_input.csv      # Sample input data
│   └── transactions_output.csv     # Processed output
├── results/
│   ├── benchmark_results.json      # Raw timing data
│   └── performance_comparison.png  # Visualization
├── tests/
│   └── test_validation.py          # Unit tests
├── requirements.txt                # Python dependencies
└── README.md                       # This file
```

## 🧪 Benchmark Methodology

### Data Generation
- **100,000 transaction records** (realistic production volume)
- **Mix of valid/invalid data** (80% valid, 20% invalid)
- **Multiple currencies** (USD, EUR, GBP, JPY)
- **Various risk levels** (high, medium, low)

### Measurement
- **5 runs per configuration** (to account for variance)
- **Averaged results** with standard deviation
- **Excludes cold start** (first run discarded)
- **Profiling enabled** to identify hotspots

### Environment
- **No background processes** during benchmarking
- **Consistent CPU frequency** (performance mode)
- **Same dataset** across all tests

## 💻 Code Example

Here's the core validation logic being benchmarked:

```python
def validate_transaction(record):
    """Validates transaction record against 47 business rules"""
    
    # Currency validation
    if record.get('currency') not in ['USD', 'EUR', 'GBP', 'JPY']:
        return False
    
    # Amount sanity checks
    amount = float(record.get('amount', 0))
    if amount <= 0 or amount > 1_000_000:
        return False
    
    # Date format normalization
    try:
        date_str = record.get('timestamp')
        parsed_date = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
    except (ValueError, TypeError):
        return False
    
    # Merchant ID validation
    merchant_id = record.get('merchant_id', '')
    if len(merchant_id) != 12 or not merchant_id.isalnum():
        return False
    
    # ... 43 more rules
    
    return True
```

## 📊 Visualization

Run `python benchmarks/visualize_results.py` to generate performance comparison charts:

![Performance Comparison](results/performance_comparison.png)

## 🤝 Contributing

Contributions welcome! Please feel free to:

- Test on different architectures (AMD, Intel, ARM)
- Add more ETL patterns (JSON processing, XML parsing, etc.)
- Compare with other optimization approaches (Numba, PyPy, Cython)
- Report issues or unexpected results

## 📚 Related Resources

- [Python 3.15 Release Notes](https://docs.python.org/3.15/whatsnew/3.15.html)
- [PEP 744: JIT Compilation](https://peps.python.org/pep-0744/)
- [Medium Article: Python's JIT Revolution](link-to-your-article)
- [CPython JIT Documentation](https://github.com/python/cpython/blob/main/Tools/jit/README.md)

## 🙏 Acknowledgments

- CPython core developers: Brandt Bucher, Mark Shannon, Ken Jin
- Python Software Foundation
- Community contributors testing and providing feedback

## 📧 Contact

Questions? Found interesting results? Open an issue or reach out:

- LinkedIn: [pravash](https://www.linkedin.com/in/pravash-panigrahi-22b19399/)
- Medium: [@pravash-techie](https://medium.com/@pravash-techie)

---

**⭐ If you find this useful, please star the repository!**

*Last updated: February 2026*
