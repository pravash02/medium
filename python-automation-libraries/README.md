# 🐍 Python Automation Libraries — Code Examples

> Companion code for the Medium article:  
> **"8 Python Libraries That Will Transform Your Automation Workflow in 2026"**

A hands-on collection of real-world code examples for 8 underrated Python libraries that experienced engineers use to build cleaner, faster, and more maintainable automation systems.

---

## 📦 Libraries Covered

| # | Library | What It Solves | Folder |
|---|---------|---------------|--------|
| 1 | [Beartype](https://beartype.readthedocs.io) | Runtime type checking without performance hit | `01_beartype/` |
| 2 | [RQ (Redis Queue)](https://python-rq.org) | Distributed task queuing, simpler than Celery | `02_rq/` |
| 3 | [PyFilesystem2](https://docs.pyfilesystem.org) | Unified API for any storage backend | `03_pyfilesystem2/` |
| 4 | [Tortoise ORM](https://tortoise.github.io) | Async database access for asyncio apps | `04_tortoise_orm/` |
| 5 | [cached-property](https://docs.python.org/3/library/functools.html#functools.cached_property) | Micro-optimization for expensive properties | `05_cached_property/` |
| 6 | [pyairtable](https://pyairtable.readthedocs.io) | Automate Airtable-powered workflows | `06_airtable/` |
| 7 | [Rich-Argparse](https://github.com/hamdanal/rich-argparse) | Beautiful CLI help pages | `07_rich_argparse/` |
| 8 | [Halo](https://github.com/manrajgrover/halo) | Terminal spinners for long-running tasks | `08_halo/` |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Redis (for RQ examples) — [install guide](https://redis.io/docs/getting-started/)
- A virtual environment (recommended)

### Installation

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/python-automation-libraries.git
cd python-automation-libraries

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows

# Install all dependencies
pip install -r requirements.txt
```

---

## 📁 Project Structure

```
python-automation-libraries/
│
├── 01_beartype/
│   ├── README.md
│   ├── basic_type_checking.py
│   ├── pipeline_contracts.py
│   └── advanced_generics.py
│
├── 02_rq/
│   ├── README.md
│   ├── basic_queue.py
│   ├── worker.py
│   ├── job_callbacks.py
│   └── scheduled_jobs.py
│
├── 03_pyfilesystem2/
│   ├── README.md
│   ├── basic_operations.py
│   ├── backend_swap.py
│   └── testing_with_memfs.py
│
├── 04_tortoise_orm/
│   ├── README.md
│   ├── models.py
│   ├── basic_crud.py
│   └── async_pipeline.py
│
├── 05_cached_property/
│   ├── README.md
│   ├── basic_caching.py
│   └── config_pattern.py
│
├── 06_airtable/
│   ├── README.md
│   ├── basic_crud.py
│   ├── sync_workflow.py
│   └── content_calendar.py
│
├── 07_rich_argparse/
│   ├── README.md
│   └── cli_runner.py
│
├── 08_halo/
│   ├── README.md
│   ├── basic_spinner.py
│   └── pipeline_with_spinner.py
│
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

## 🔐 Environment Variables

Copy `.env.example` to `.env` and fill in your credentials:

```bash
cp .env.example .env
```

Required for Airtable examples:
```
AIRTABLE_API_KEY=your_api_key_here
AIRTABLE_BASE_ID=appXXXXXXXXXXXXXX
```

---

## 🤝 Contributing

Found a bug or want to add an example? PRs are welcome!

1. Fork the repo
2. Create your branch: `git checkout -b feature/add-example`
3. Commit your changes: `git commit -m 'Add example for X'`
4. Push and open a Pull Request

---

## 📄 License

MIT — use freely, attribution appreciated.

---

## ✍️ Author

Built with ❤️ to accompany the Medium article series on Python automation.  
**Follow on Medium** for weekly Python tooling deep-dives.
