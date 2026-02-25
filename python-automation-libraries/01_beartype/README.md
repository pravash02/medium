# 01 — Beartype: Runtime Type Checking Without the Pain

Beartype performs **O(1) runtime type checking** — validating types at function boundaries
without slowing down your application, even in production.

## Run the Examples

```bash
python basic_type_checking.py
python pipeline_contracts.py
python advanced_generics.py
```

## Key Concepts

- `@beartype` decorator enforces type hints at runtime
- Raises `BeartypeException` (not `TypeError`) for clarity
- Supports all Python typing constructs: `Union`, `Optional`, `List[str]`, etc.
- Works alongside `mypy` and `pyright` — does not replace them

## When to Use

- Ingesting data from external APIs or files
- Enforcing contracts at module boundaries
- Catching type mismatches that slip past static analysis
