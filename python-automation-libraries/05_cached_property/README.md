# 05 — cached_property: The Micro-Optimization You're Probably Missing

`functools.cached_property` (Python 3.8+) computes a property once,
caches the result on the instance, and returns it instantly on every
subsequent access — no external libraries required.

## Run the Examples

```bash
python basic_caching.py
python config_pattern.py
```

## Key Concepts

- Built into Python 3.8+ via `functools.cached_property`
- Stores result in instance `__dict__` — O(1) lookup after first call
- Computed lazily — only runs when first accessed
- Not thread-safe by default (use `threading.Lock` if needed)
- To invalidate: `del instance.property_name`
