"""
04_tortoise_orm/basic_crud.py
-------------------------------
Tortoise ORM: define models, initialize DB, perform async CRUD.
Uses SQLite (aiosqlite) — no database server needed.
"""

import asyncio
from tortoise import Tortoise, fields
from tortoise.models import Model
from tortoise.expressions import Q


#  Models 

class Pipeline(Model):
    id          = fields.IntField(pk=True)
    name        = fields.CharField(max_length=100)
    status      = fields.CharField(max_length=20, default="pending")
    is_active   = fields.BooleanField(default=True)
    created_at  = fields.DatetimeField(auto_now_add=True)
    updated_at  = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "pipelines"

    def __str__(self):
        return f"<Pipeline #{self.id}: {self.name} [{self.status}]>"


class JobRecord(Model):
    id          = fields.IntField(pk=True)
    pipeline    = fields.ForeignKeyField("models.Pipeline", related_name="jobs")
    url         = fields.TextField()
    status      = fields.CharField(max_length=20, default="pending")
    retries     = fields.IntField(default=0)
    result      = fields.JSONField(null=True)
    created_at  = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "job_records"


#  DB Init ─

async def init_db(db_url: str = "sqlite://:memory:"):
    """Initialize Tortoise ORM with the given DB URL."""
    await Tortoise.init(
        db_url=db_url,
        modules={"models": ["__main__"]},
    )
    await Tortoise.generate_schemas()


#  CRUD operations ─

async def demo_crud():
    print("=" * 55)
    print("TORTOISE ORM — Basic CRUD")
    print("=" * 55)

    #  CREATE 
    print("\n CREATE \n")

    etl_pipeline = await Pipeline.create(name="Daily ETL", status="running")
    scraper      = await Pipeline.create(name="Web Scraper", status="pending")
    reporter     = await Pipeline.create(name="Report Generator", status="completed")

    print(f"  Created: {etl_pipeline}")
    print(f"  Created: {scraper}")
    print(f"  Created: {reporter}")

    # Create related jobs
    await JobRecord.create(pipeline=etl_pipeline, url="https://api.example.com/data/v1")
    await JobRecord.create(pipeline=etl_pipeline, url="https://api.example.com/data/v2")
    await JobRecord.create(pipeline=scraper,       url="https://target.com/products")

    #  READ 
    print("\n READ \n")

    # Fetch all
    all_pipelines = await Pipeline.all()
    print(f"  All pipelines ({len(all_pipelines)}):")
    for p in all_pipelines:
        print(f"    {p}")

    # Filter
    running = await Pipeline.filter(status="running").all()
    print(f"\n  Running pipelines: {[p.name for p in running]}")

    # Complex filter with Q objects (OR condition)
    active = await Pipeline.filter(
        Q(status="running") | Q(status="pending")
    ).all()
    print(f"  Active (running OR pending): {[p.name for p in active]}")

    # Get single record
    etl = await Pipeline.get(name="Daily ETL")
    print(f"\n  Fetched by name: {etl}")

    # Fetch with related jobs
    pipeline_with_jobs = await Pipeline.get(id=etl_pipeline.id).prefetch_related("jobs")
    print(f"\n  Jobs for '{pipeline_with_jobs.name}':")
    for job in pipeline_with_jobs.jobs:
        print(f"    → {job.url} [{job.status}]")

    #  UPDATE 
    print("\n UPDATE \n")

    etl_pipeline.status = "completed"
    await etl_pipeline.save()
    print(f"  Updated: {etl_pipeline}")

    # Bulk update
    updated_count = await Pipeline.filter(status="pending").update(is_active=False)
    print(f"  Bulk update: {updated_count} pipeline(s) set to inactive")

    #  DELETE 
    print("\n DELETE \n")

    await reporter.delete()
    print(f"  Deleted: Report Generator")

    remaining = await Pipeline.all().count()
    print(f"  Remaining pipelines: {remaining}")

    #  AGGREGATE ─
    print("\n AGGREGATE \n")

    total         = await Pipeline.all().count()
    completed     = await Pipeline.filter(status="completed").count()
    job_count     = await JobRecord.all().count()

    print(f"  Total pipelines:    {total}")
    print(f"  Completed:          {completed}")
    print(f"  Total job records:  {job_count}")


#  Main 

async def main():
    await init_db()
    try:
        await demo_crud()
    finally:
        await Tortoise.close_connections()
    print("\n Done — connections closed.")


if __name__ == "__main__":
    asyncio.run(main())
