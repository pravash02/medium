"""
02_rq/basic_queue.py
----------------------
Basic RQ usage: enqueue jobs, check status, fetch results.
Requires Redis running on localhost:6379.
Run a worker first: `rq worker` in another terminal.
"""

import time
from redis import Redis
from rq import Queue
from rq.job import Job


#  Task functions (must be importable by the worker)
def scrape_and_store(url: str) -> dict:
    """Simulates scraping a URL. In production, use requests + BeautifulSoup."""
    time.sleep(1)  # Simulate network latency
    return {
        "url": url,
        "status": 200,
        "word_count": 1_423,
        "scraped_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
    }


def send_report_email(recipient: str, subject: str, body: str) -> bool:
    """Simulates sending an email report."""
    time.sleep(0.5)
    print(f"  [worker] Email sent to {recipient}: '{subject}'")
    return True


def process_csv_file(filepath: str, delimiter: str = ",") -> dict:
    """Simulates processing a CSV file."""
    time.sleep(0.8)
    return {"filepath": filepath, "rows_processed": 1_042, "errors": 0}


#  Queue setup
def get_queue(queue_name: str = "default") -> Queue:
    """Returns an RQ Queue connected to local Redis."""
    redis_conn = Redis(host="localhost", port=6379, db=0)
    return Queue(queue_name, connection=redis_conn)


#  Demo
def main():
    print("=" * 55)
    print("RQ — Basic Queue Example")
    print("=" * 55)

    q = get_queue()

    print(f"\nQueue: '{q.name}' | Jobs before: {len(q)}")

    # Enqueue jobs
    print("\nEnqueueing jobs...\n")

    job1 = q.enqueue(scrape_and_store, "https://example.com/products")
    job2 = q.enqueue(scrape_and_store, "https://example.com/blog")
    job3 = q.enqueue(
        send_report_email,
        recipient="team@company.com",
        subject="Daily Automation Report",
        body="Pipeline ran successfully.",
    )
    job4 = q.enqueue(
        process_csv_file,
        filepath="/data/sales_q4.csv",
        delimiter=";",
        job_timeout=60,      # Max 60 seconds before job is killed
        result_ttl=3600,     # Keep result in Redis for 1 hour
    )

    jobs = [job1, job2, job3, job4]
    for job in jobs:
        print(f"  ✓ Enqueued job {job.id[:8]}... → {job.func_name}")

    print(f"\nQueue depth now: {len(q)} jobs")
    print("\n Start a worker to process these: `rq worker`")

    # Poll for results (if worker is running)
    print("\nPolling for job1 result (10s timeout)...\n")
    timeout = 10
    start = time.time()
    while time.time() - start < timeout:
        job1.refresh()
        if job1.is_finished:
            print(f" job1 result: {job1.result}")
            break
        if job1.is_failed:
            print(f" job1 failed: {job1.exc_info}")
            break
        print(f"  Status: {job1.get_status()} — waiting...")
        time.sleep(1)
    else:
        print(" No worker running — jobs queued and waiting.")


if __name__ == "__main__":
    main()
