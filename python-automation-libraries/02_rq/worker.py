"""
02_rq/worker.py
-----------------
Custom RQ worker with connection setup and graceful shutdown.
Run with: python worker.py
Or use the CLI: rq worker [queue_name]
"""

import logging
import os
from redis import Redis
from rq import Worker, Queue, Connection

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


def create_worker(queues: list[str] | None = None):
    """
    Creates and starts an RQ worker.

    Args:
        queues: List of queue names to listen on. Priority order matters —
                worker processes queues left-to-right. Defaults to ['high', 'default', 'low'].
    """
    redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
    conn = Redis.from_url(redis_url)

    listen_queues = queues or ["high", "default", "low"]
    logger.info(f"Starting worker — listening on queues: {listen_queues}")

    with Connection(conn):
        worker = Worker(
            queues=[Queue(q, connection=conn) for q in listen_queues],
            connection=conn,
            log_job_description=True,
        )
        worker.work(with_scheduler=True)  # with_scheduler enables RQ Scheduler


if __name__ == "__main__":
    create_worker()
