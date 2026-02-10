# Python Productivity Libraries: Benchmarks & Examples

> Real-world performance tests and production-ready examples for 6 underutilized Python libraries

[![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## 📊 Performance Results

| Library | Use Case | Improvement | Status |
|---------|----------|-------------|--------|
| **FlashText** | Keyword replacement | 120x faster than regex | ✅ Production |
| **UJson** | JSON parsing | 62% faster than json | ✅ Production |
| **Tenacity** | API retry logic | 98% failure reduction | ✅ Production |
| **Dataset** | SQL operations | 12x faster prototyping | ⚠️ Prototype only |
| **Pyexcel** | Excel processing | Auto-format detection | ✅ Production |
| **Langextract** | Text extraction | 70% less code | ✅ Production |

## 🚀 Quick Start

```bash
# Clone Repository
git clone https://github.com/yourusername/python-productivity-libraries
cd python-productivity-libraries

# Install Dependencies
pip install -r requirements.txt

# Run All Benchmarks
python benchmarks/run_all.py

# Run Specific Benchmark
python benchmarks/flashtext_benchmark.py
```

## 📁 Repository Structure

```
python-productivity-libraries/
├── benchmarks/              # Performance benchmarks
│   ├── flashtext_benchmark.py
│   ├── ujson_benchmark.py
│   ├── tenacity_benchmark.py
│   └── run_all.py
├── examples/                # Production-ready examples
│   ├── flashtext_example.py
│   ├── ujson_example.py
│   ├── tenacity_example.py
│   ├── dataset_example.py
│   ├── pyexcel_example.py
│   └── langextract_example.py
├── data/                    # Sample data files
│   ├── sample_text.txt
│   ├── sample_json.json
│   └── sample_excel.xlsx
├── tests/                   # Unit tests
└── requirements.txt
```

## 📚 Library Deep Dives

### 1. FlashText - 120x Faster Keyword Replacement

**When to use:** 50+ keywords, large text volumes, exact matches

```python
from flashtext import KeywordProcessor

processor = KeywordProcessor()
processor.add_keyword('Python', 'Python 3.12')
result = processor.replace_keywords("I love Python programming")
# "I love Python 3.12 programming"
```

**Benchmark:** `python benchmarks/flashtext_benchmark.py`

### 2. UJson - 62% Faster JSON Parsing

**When to use:** Large JSON files, high-throughput APIs, batch processing

```python
import ujson

data = ujson.loads('{"key": "value"}')
# 60% faster than json.loads()
```

**Benchmark:** `python benchmarks/ujson_benchmark.py`

### 3. Tenacity - Intelligent Retry Logic

**When to use:** External APIs, database operations, network calls

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential())
def api_call():
    return requests.get('https://api.example.com/data')
```

**Benchmark:** `python benchmarks/tenacity_benchmark.py`

### 4. Dataset - SQL Without ORM Overhead

**When to use:** Prototyping, ETL scripts, ad-hoc queries

```python
import dataset

db = dataset.connect('sqlite:///mydb.db')
db['users'].insert(dict(name='John', age=30))
```

**Example:** `python examples/dataset_example.py`

### 5. Pyexcel - Universal Excel Handler

**When to use:** Multi-format Excel processing, user uploads

```python
import pyexcel as pe

data = pe.get_array(file_name="data.xlsx")
```

**Example:** `python examples/pyexcel_example.py`

### 6. Langextract - Structured Data Extraction

**When to use:** Log analysis, support tickets, text mining

```python
from langextract import Extractor

extractor = Extractor(patterns={"date": r"\d{4}-\d{2}-\d{2}"})
results = extractor.extract("Report from 2026-02-09")
```

**Example:** `python examples/langextract_example.py`

## 🧪 Running Benchmarks

### All Benchmarks
```bash
python benchmarks/run_all.py
```

### Individual Benchmarks
```bash
# FlashText vs Regex
python benchmarks/flashtext_benchmark.py

# UJson vs Standard JSON
python benchmarks/ujson_benchmark.py

# Tenacity retry patterns
python benchmarks/tenacity_benchmark.py
```

## 📈 Expected Results

On a typical development machine (8-core CPU, 16GB RAM):

```
=== FlashText Benchmark ===
Regex time: 48.32s
FlashText time: 0.40s
Speedup: 120.8x

=== UJson Benchmark ===
Standard json: 1.847s
UJson: 0.723s
Improvement: 60.9%

=== Tenacity Benchmark ===
Without retry: 85% success rate
With Tenacity: 99.8% success rate
```

## 🤝 Contributing

Found better performance? Have production examples to share?

1. Fork the repository
2. Create a feature branch
3. Add your benchmark/example
4. Submit a pull request

We especially welcome:
- Real-world use cases
- Performance comparisons on different hardware
- Production gotchas and solutions

## 🔗 Related Resources

- [Medium Article: 6 Python Libraries That Slashed My Processing Time by 40%](link-to-article)
- [FlashText Documentation](https://github.com/vi3k6i5/flashtext)
- [UJson Documentation](https://github.com/ultrajson/ultrajson)
- [Tenacity Documentation](https://tenacity.readthedocs.io/)

## 📧 Contact

Questions? Suggestions? Open an issue or reach out:
- LinkedIn: [pravash](https://www.linkedin.com/in/pravash-panigrahi-22b19399/)
- Medium: [@pravash-techie](https://medium.com/@pravash-techie)

---

⭐ **If you find this useful, please star the repository!**

*Last updated: February 2026*
