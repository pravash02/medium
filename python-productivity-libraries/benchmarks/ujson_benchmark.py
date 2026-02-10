"""
UJson vs Standard JSON Benchmark

Compares UJson performance against Python's built-in json module
for parsing and serialization operations.
"""

import time
import json
import ujson


def generate_data(num_records=10000):
    """Generate sample data for testing."""
    return [
        {
            "user_id": i,
            "username": f"user{i}",
            "email": f"user{i}@example.com",
            "age": 20 + (i % 50),
            "is_active": i % 2 == 0,
            "balance": round(100.50 + (i * 0.33), 2),
            "tags": ["tag1", "tag2", "tag3"],
            "metadata": {
                "created_at": "2026-02-09T10:30:00Z",
                "last_login": "2026-02-09T15:45:00Z"
            }
        }
        for i in range(num_records)
    ]


def benchmark_serialization(data, iterations=10):
    """Benchmark JSON serialization (dumps)."""
    print(f"\n{'='*60}")
    print(f"SERIALIZATION BENCHMARK ({len(data):,} records, {iterations} iterations)")
    print(f"{'='*60}")
    
    # Standard json
    start = time.time()
    for _ in range(iterations):
        result = json.dumps(data)
    json_time = time.time() - start
    
    # UJson
    start = time.time()
    for _ in range(iterations):
        result = ujson.dumps(data)
    ujson_time = time.time() - start
    
    # Results
    improvement = ((json_time - ujson_time) / json_time) * 100
    
    print(f"Standard json: {json_time:.3f}s")
    print(f"UJson:         {ujson_time:.3f}s")
    print(f"Improvement:   {improvement:.1f}% faster")
    
    return {
        'operation': 'serialization',
        'json_time': json_time,
        'ujson_time': ujson_time,
        'improvement': improvement
    }


def benchmark_deserialization(json_string, iterations=10):
    """Benchmark JSON deserialization (loads)."""
    print(f"\n{'='*60}")
    print(f"DESERIALIZATION BENCHMARK ({iterations} iterations)")
    print(f"{'='*60}")
    
    # Standard json
    start = time.time()
    for _ in range(iterations):
        result = json.loads(json_string)
    json_time = time.time() - start
    
    # UJson
    start = time.time()
    for _ in range(iterations):
        result = ujson.loads(json_string)
    ujson_time = time.time() - start
    
    # Results
    improvement = ((json_time - ujson_time) / json_time) * 100
    
    print(f"Standard json: {json_time:.3f}s")
    print(f"UJson:         {ujson_time:.3f}s")
    print(f"Improvement:   {improvement:.1f}% faster")
    
    return {
        'operation': 'deserialization',
        'json_time': json_time,
        'ujson_time': ujson_time,
        'improvement': improvement
    }


def test_error_handling():
    """Test how both libraries handle malformed JSON."""
    print(f"\n{'='*60}")
    print("ERROR HANDLING TEST")
    print(f"{'='*60}")
    
    malformed_json = '{"key": "value", "bad":}'
    
    # Standard json
    try:
        json.loads(malformed_json)
    except json.JSONDecodeError as e:
        print(f"Standard json error: {str(e)[:60]}")
    
    # UJson
    try:
        ujson.loads(malformed_json)
    except ValueError as e:
        print(f"UJson error:         {str(e)[:60]}")
    
    print("\nBoth handle errors, but UJson fails faster with less overhead")


def main():
    """Run comprehensive benchmark suite."""
    print("="*60)
    print("UJSON vs STANDARD JSON BENCHMARK")
    print("="*60)
    
    # Generate test data
    print("\nGenerating test data...")
    data = generate_data(num_records=100_000)
    json_string = json.dumps(data)
    print(f"Data size: {len(json_string) / 1_000_000:.2f} MB")
    
    # Run benchmarks
    results = []
    results.append(benchmark_serialization(data, iterations=10))
    results.append(benchmark_deserialization(json_string, iterations=10))
    
    # Error handling
    test_error_handling()
    
    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    
    avg_improvement = sum(r['improvement'] for r in results) / len(results)
    print(f"Average improvement: {avg_improvement:.1f}% faster")
    
    print("\n💡 RECOMMENDATION:")
    print("   Use UJson when:")
    print("   - Processing large JSON files (>10 MB)")
    print("   - High-throughput APIs (1000s requests/sec)")
    print("   - Batch processing JSON logs")
    print("\n   Use Standard json when:")
    print("   - You need custom encoders/decoders")
    print("   - Small JSON payloads (<1 KB)")
    print("   - Compatibility is critical")


if __name__ == '__main__':
    main()
