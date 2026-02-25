# 04 — Tortoise ORM: Async Database Automation Without Tears

Tortoise ORM is an async Python ORM inspired by Django ORM. Built for
asyncio — works with FastAPI, aiohttp, and any async pipeline.

## Run the Examples

```bash
python basic_crud.py
python async_pipeline.py
```

## Supported Databases

| Database   | Driver      | Install              |
|-----------|-------------|----------------------|
| SQLite    | aiosqlite   | `pip install aiosqlite` |
| PostgreSQL | asyncpg    | `pip install asyncpg`   |
| MySQL     | aiomysql    | `pip install aiomysql`  |

## Key Concepts

- `Tortoise.init()` — initialize ORM with DB URL and models
- `await Model.create(...)` — async INSERT
- `await Model.filter(...).all()` — async SELECT
- `await obj.save()` — async UPDATE
- `await obj.delete()` — async DELETE
- `await Tortoise.generate_schemas()` — create tables from models
