import random
import time
import logging
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    wait_fixed,
    retry_if_exception_type,
    retry_if_result,
    before_sleep_log,
    after_log
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class RateLimitError(Exception):
    pass


class ServiceUnavailableError(Exception):
    pass


def simulate_flaky_api(success_rate=0.4):
    if random.random() > success_rate:
        error_type = random.choice([
            RateLimitError("429: Too Many Requests"),
            ServiceUnavailableError("503: Service Unavailable"),
            ConnectionError("Network timeout"),
        ])
        raise error_type
    return {"status": "success", "data": {"user_id": 42, "balance": 1500.00}}


def simulate_flaky_db(success_rate=0.7):
    if random.random() > success_rate:
        raise TimeoutError("Database connection timed out")
    return True


@retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=1, min=1, max=10),
    retry=retry_if_exception_type((
        RateLimitError,
        ServiceUnavailableError,
        ConnectionError,
    )),
    before_sleep=before_sleep_log(logger, logging.WARNING),
    reraise=True
)
def fetch_user_data(user_id):
    logger.info(f"Fetching data for user {user_id}...")
    return simulate_flaky_api(success_rate=0.5)


@retry(
    stop=stop_after_attempt(3),
    wait=wait_fixed(2),
    retry=retry_if_exception_type(TimeoutError),
    # ValueError = bad data → don't retry, it won't fix itself
)
def save_transaction(transaction_id, amount):
    if amount <= 0:
        raise ValueError(f"Invalid amount: {amount}")  # Won't retry
    logger.info(f"Saving transaction {transaction_id}...")
    simulate_flaky_db(success_rate=0.6)
    return {"transaction_id": transaction_id, "status": "saved"}


def is_job_incomplete(result):
    return result.get('status') != 'completed'


@retry(
    stop=stop_after_attempt(10),
    wait=wait_fixed(1),
    retry=retry_if_result(is_job_incomplete),
)
def poll_job_status(job_id):
    statuses = ['pending', 'pending', 'processing', 'processing', 'completed']
    status = random.choice(statuses)
    logger.info(f"Job {job_id} status: {status}")
    return {"job_id": job_id, "status": status}


def process_records_with_retry(records):
    results = {'success': [], 'failed': []}

    for record in records:
        try:
            result = fetch_user_data(record['user_id'])
            results['success'].append({
                'user_id': record['user_id'],
                'data': result
            })
        except Exception as e:
            logger.error(f"Failed after retries for user {record['user_id']}: {e}")
            results['failed'].append({
                'user_id': record['user_id'],
                'error': str(e)
            })

    return results


def main():
    print("=" * 60)
    print("Tenacity: Production Retry Patterns")
    print("=" * 60)

    random.seed(42)  # Reproducible results

    print("\n--- Example 1: API Retry with Exponential Backoff ---")
    try:
        result = fetch_user_data(user_id=101)
        print(f"Success: {result}")
    except Exception as e:
        print(f"Failed after all retries: {e}")

    print("\n--- Example 2: Database Retry (Transient Only) ---")
    try:
        result = save_transaction("TXN-001", amount=250.00)
        print(f"Saved: {result}")
    except TimeoutError:
        print("DB unavailable after retries")

    print("\n--- Example 2b: Bad Data (No Retry) ---")
    try:
        save_transaction("TXN-002", amount=-50)
    except ValueError as e:
        print(f"Correctly rejected bad data (no retry): {e}")

    print("\n--- Example 3: Poll Job Until Completed ---")
    try:
        result = poll_job_status(job_id="JOB-789")
        print(f"Job completed: {result}")
    except Exception as e:
        print(f"Job timed out: {e}")

    print("\n--- Example 4: Batch Processing with Per-Record Retry ---")
    records = [{'user_id': i} for i in range(1, 6)]
    results = process_records_with_retry(records)
    print(f"\nBatch Results:")
    print(f"  Success : {len(results['success'])}")
    print(f"  Failed  : {len(results['failed'])}")


if __name__ == '__main__':
    main()
