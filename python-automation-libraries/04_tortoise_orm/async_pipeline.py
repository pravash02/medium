"""
04_tortoise_orm/async_pipeline.py
------------------------------------
Real-world pattern: async ETL pipeline using Tortoise ORM.
Concurrent record processing with asyncio.gather().
"""

import asyncio
import random
import time
from tortoise import Tortoise, fields
from tortoise.models import Model


#  Models 

class DataSource(Model):
    id       = fields.IntField(pk=True)
    name     = fields.CharField(max_length=100)
    endpoint = fields.TextField()

    class Meta:
        table = "data_sources"


class FetchedRecord(Model):
    id         = fields.IntField(pk=True)
    source     = fields.ForeignKeyField("models.DataSource", related_name="records")
    raw_data   = fields.JSONField()
    processed  = fields.BooleanField(default=False)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "fetched_records"


#  Simulated async I/O ─

async def fetch_from_api(endpoint: str) -> list[dict]:
    """Simulates an async HTTP call."""
    await asyncio.sleep(random.uniform(0.1, 0.4))
    return [
        {"endpoint": endpoint, "value": random.randint(100, 999), "seq": i}
        for i in range(1, random.randint(3, 6))
    ]


async def transform_record(record: dict) -> dict:
    """Applies transformation asynchronously."""
    await asyncio.sleep(0.05)
    return {**record, "value_doubled": record["value"] * 2, "processed": True}


#  Pipeline stages ─

async def fetch_and_store(source: DataSource) -> int:
    """Fetch from API and persist raw records."""
    raw_data = await fetch_from_api(source.endpoint)
    records  = [
        FetchedRecord(source=source, raw_data=item)
        for item in raw_data
    ]
    await FetchedRecord.bulk_create(records)
    print(f"  ✓ [{source.name}] Fetched and stored {len(records)} records")
    return len(records)


async def process_pending_records() -> int:
    """Transform all unprocessed records — runs concurrently."""
    pending = await FetchedRecord.filter(processed=False).all()
    if not pending:
        return 0

    async def process_one(record: FetchedRecord):
        transformed = await transform_record(record.raw_data)
        record.raw_data  = transformed
        record.processed = True
        await record.save()

    await asyncio.gather(*[process_one(r) for r in pending])
    print(f"  Processed {len(pending)} records concurrently")
    return len(pending)


#  Full pipeline ─

async def run_pipeline():
    print("=" * 55)
    print("TORTOISE ORM — Async Pipeline Demo")
    print("=" * 55)

    await Tortoise.init(
        db_url="sqlite://:memory:",
        modules={"models": ["__main__"]},
    )
    await Tortoise.generate_schemas()

    # Seed data sources
    sources = await DataSource.bulk_create([
        DataSource(name="Inventory API",   endpoint="https://api.example.com/inventory"),
        DataSource(name="Orders API",      endpoint="https://api.example.com/orders"),
        DataSource(name="Customers API",   endpoint="https://api.example.com/customers"),
    ])
    print(f"\nSeeded {len(sources)} data sources\n")

    #  Stage 1: Concurrent fetch from all sources 
    print(" Stage 1: Concurrent fetch \n")
    start = time.perf_counter()

    fetch_tasks = [fetch_and_store(source) for source in sources]
    counts = await asyncio.gather(*fetch_tasks)

    elapsed = time.perf_counter() - start
    total_fetched = sum(counts)
    print(f"\n  Total fetched: {total_fetched} records in {elapsed:.2f}s (concurrent)")

    #  Stage 2: Process all records 
    print("\n Stage 2: Parallel processing \n")
    start = time.perf_counter()
    processed = await process_pending_records()
    elapsed = time.perf_counter() - start
    print(f"\n  Processed {processed} records in {elapsed:.2f}s")

    #  Stage 3: Summary report ─
    print("\n Stage 3: Summary \n")
    for source in sources:
        count = await FetchedRecord.filter(source=source, processed=True).count()
        print(f"  {source.name:20s} → {count} records processed")

    total = await FetchedRecord.filter(processed=True).count()
    print(f"\n  Pipeline complete. {total} total records in DB.")

    await Tortoise.close_connections()


if __name__ == "__main__":
    asyncio.run(run_pipeline())
