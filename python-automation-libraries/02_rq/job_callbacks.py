"""
02_rq/job_callbacks.py
------------------------
Advanced RQ patterns: job chaining, success/failure callbacks,
priority queues, and job dependencies.
"""

import time
from redis import Redis
from rq import Queue, Callback
from rq.job import Job


#  Task functions 
def fetch_data(source_id: int) -> list[dict]:
    """Stage 1: Fetch raw records."""
    time.sleep(0.5)
    return [{"id": i, "value": i * 10} for i in range(1, source_id + 1)]


def transform_data(records: list[dict]) -> list[dict]:
    """Stage 2: Apply transformation."""
    time.sleep(0.3)
    return [{"id": r["id"], "value": r["value"] * 1.15, "processed": True} for r in records]


def load_to_db(records: list[dict]) -> dict:
    """Stage 3: Persist to database."""
    time.sleep(0.2)
    return {"inserted": len(records), "status": "success"}


#  Callback functions 
def on_success(job: Job, connection, result, *args, **kwargs):
    """Called when a job completes successfully."""
    print(f" SUCCESS  Job {job.id[:8]}... returned: {result}")


def on_failure(job: Job, connection, type, value, traceback):
    """Called when a job fails. Use for alerting, retry logic, or logging."""
    print(f" FAILURE  Job {job.id[:8]}... failed with {type.__name__}: {value}")


def on_stopped(job: Job, connection):
    """Called when a job is manually stopped."""
    print(f" STOPPED  Job {job.id[:8]}... was cancelled.")


#  Priority queues
def setup_priority_queues(conn: Redis) -> dict[str, Queue]:
    """Create high/default/low priority queues."""
    return {
        "high":    Queue("high",    connection=conn),
        "default": Queue("default", connection=conn),
        "low":     Queue("low",     connection=conn),
    }


#  Demo
def main():
    print("=" * 55)
    print("RQ  Callbacks & Job Chaining Example")
    print("=" * 55)

    conn = Redis(host="localhost", port=6379)
    queues = setup_priority_queues(conn)

    #  1. Job with success/failure callbacks 
    print("\n Enqueue with callbacks \n")
    job = queues["default"].enqueue(
        fetch_data,
        5,
        on_success=Callback(on_success),
        on_failure=Callback(on_failure),
        on_stopped=Callback(on_stopped),
    )
    print(f"  Enqueued: {job.id[:8]}... → fetch_data(5)")

    #  2. Job dependency chaining (ETL pipeline) 
    print("\n ETL chain: fetch → transform → load \n")

    # Job 1: fetch
    j_fetch = queues["high"].enqueue(fetch_data, 10)
    print(f"  [1] fetch_data enqueued    → {j_fetch.id[:8]}...")

    # Job 2: transform depends on fetch completing
    j_transform = queues["high"].enqueue(
        transform_data,
        depends_on=j_fetch,      # Won't run until j_fetch completes
    )
    print(f"  [2] transform_data queued  → {j_transform.id[:8]}... (depends on step 1)")

    # Job 3: load depends on transform
    j_load = queues["high"].enqueue(
        load_to_db,
        depends_on=j_transform,  # Won't run until j_transform completes
        on_success=Callback(on_success),
    )
    print(f"  [3] load_to_db queued      → {j_load.id[:8]}... (depends on step 2)")

    #  3. Priority queue demo 
    print("\n Priority queue example \n")
    queues["low"].enqueue(fetch_data, 1)
    queues["default"].enqueue(fetch_data, 2)
    queues["high"].enqueue(fetch_data, 3)

    print("  Enqueued to low / default / high queues.")
    print("  Worker (rq worker high default low) processes high-priority first.")

    print("\n Run `rq worker high default low` to process the chain.")


if __name__ == "__main__":
    main()
