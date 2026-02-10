import json
import ujson
import time
from datetime import datetime


SAMPLE_LOGS = [
    '{"user_id": 1001, "event": "login", "timestamp": "2026-02-09T10:30:00Z", "ip": "192.168.1.1", "status": 200}',
    '{"user_id": 1002, "event": "purchase", "timestamp": "2026-02-09T10:31:00Z", "amount": 149.99, "product_id": "P001"}',
    '{"user_id": 1003, "event": "page_view", "timestamp": "2026-02-09T10:32:00Z", "page": "/products", "duration_ms": 320}',
    '{"user_id": 1001, "event": "logout", "timestamp": "2026-02-09T10:45:00Z", "session_duration": 900}',
    '{"user_id": 1004, "event": "signup", "timestamp": "2026-02-09T10:46:00Z", "referrer": "google", "plan": "pro"}',
]


def parse_logs_standard(logs):
    parsed = []
    for log in logs:
        try:
            parsed.append(json.loads(log))
        except json.JSONDecodeError:
            continue
    return parsed


def parse_logs_ujson(logs):
    parsed = []
    for log in logs:
        try:
            parsed.append(ujson.loads(log))
        except ValueError:
            continue
    return parsed


def process_event_pipeline(logs):
    events = {
        'logins': [],
        'purchases': [],
        'page_views': [],
        'signups': [],
        'other': []
    }

    total_revenue = 0.0
    error_count = 0

    for raw_log in logs:
        try:
            event = ujson.loads(raw_log)

            event_type = event.get('event', 'unknown')

            if event_type == 'login':
                events['logins'].append(event['user_id'])

            elif event_type == 'purchase':
                amount = float(event.get('amount', 0))
                total_revenue += amount
                events['purchases'].append({
                    'user_id': event['user_id'],
                    'amount': amount,
                    'product_id': event.get('product_id')
                })

            elif event_type == 'page_view':
                events['page_views'].append(event.get('page', '/'))

            elif event_type == 'signup':
                events['signups'].append({
                    'user_id': event['user_id'],
                    'plan': event.get('plan', 'free')
                })

            else:
                events['other'].append(event)

        except (ValueError, KeyError) as e:
            error_count += 1
            continue

    return {
        'summary': {
            'total_events': len(logs),
            'total_logins': len(events['logins']),
            'total_purchases': len(events['purchases']),
            'total_page_views': len(events['page_views']),
            'total_signups': len(events['signups']),
            'total_revenue': round(total_revenue, 2),
            'error_count': error_count
        },
        'events': events
    }


def benchmark_parsers(logs, iterations=1000):
    print("\n" + "=" * 60)
    print(f"BENCHMARK: {len(logs)} logs x {iterations} iterations")
    print("=" * 60)

    start = time.time()
    for _ in range(iterations):
        parse_logs_standard(logs)
    json_time = time.time() - start

    start = time.time()
    for _ in range(iterations):
        parse_logs_ujson(logs)
    ujson_time = time.time() - start

    improvement = ((json_time - ujson_time) / json_time) * 100

    print(f"Standard json : {json_time:.3f}s")
    print(f"UJson         : {ujson_time:.3f}s")
    print(f"Improvement   : {improvement:.1f}% faster")


def main():
    print("=" * 60)
    print("UJson: Production API Log Processing")
    print("=" * 60)

    print("\nProcessing event logs...")
    result = process_event_pipeline(SAMPLE_LOGS)

    print("\nPipeline Summary:")
    print("-" * 40)
    for key, value in result['summary'].items():
        print(f"  {key:<25}: {value}")

    output = ujson.dumps(result['summary'], indent=2)
    print(f"\nJSON Output (UJson):\n{output}")

    large_logs = SAMPLE_LOGS * 200  # 1,000 logs
    benchmark_parsers(large_logs, iterations=100)


if __name__ == '__main__':
    main()
