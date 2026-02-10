"""
FlashText vs Regex Benchmark

Compares FlashText keyword replacement performance against regex
on varying dataset sizes and keyword counts.
"""

import time
import re
from flashtext import KeywordProcessor


def generate_text(num_words=1000):
    """Generate sample text for testing."""
    words = [
        "Python", "JavaScript", "Java", "C++", "Ruby", "Go", "Rust",
        "programming", "development", "software", "code", "algorithm"
    ]
    return " ".join([words[i % len(words)] for i in range(num_words)])


def regex_replace(text, replacements):
    """Replace keywords using regex."""
    pattern = re.compile('|'.join(re.escape(k) for k in replacements.keys()))
    return pattern.sub(lambda m: replacements[m.group()], text)


def flashtext_replace(text, replacements):
    """Replace keywords using FlashText."""
    processor = KeywordProcessor()
    for old, new in replacements.items():
        processor.add_keyword(old, new)
    return processor.replace_keywords(text)


def run_benchmark(text_size, num_keywords):
    """Run benchmark with specified parameters."""
    print(f"\n{'='*60}")
    print(f"Text size: {text_size:,} words | Keywords: {num_keywords}")
    print(f"{'='*60}")
    
    # Generate test data
    text = generate_text(text_size)
    
    # Create keyword replacements
    replacements = {
        f"keyword{i}": f"REPLACED{i}" for i in range(num_keywords)
    }
    # Add some actual keywords that exist in text
    replacements.update({
        "Python": "Python 3.12",
        "JavaScript": "JavaScript ES2024",
        "programming": "software development"
    })
    
    # Benchmark regex
    start = time.time()
    regex_result = regex_replace(text, replacements)
    regex_time = time.time() - start
    
    # Benchmark FlashText
    start = time.time()
    flashtext_result = regex_replace(text, replacements)
    flashtext_time = time.time() - start
    
    # Results
    speedup = regex_time / flashtext_time if flashtext_time > 0 else float('inf')
    
    print(f"Regex time:     {regex_time:.4f}s")
    print(f"FlashText time: {flashtext_time:.4f}s")
    print(f"Speedup:        {speedup:.1f}x faster")
    
    return {
        'text_size': text_size,
        'num_keywords': num_keywords,
        'regex_time': regex_time,
        'flashtext_time': flashtext_time,
        'speedup': speedup
    }


def main():
    """Run comprehensive benchmark suite."""
    print("="*60)
    print("FLASHTEXT vs REGEX BENCHMARK")
    print("="*60)
    
    results = []
    
    # Scenario 1: Small text, few keywords
    results.append(run_benchmark(text_size=1_000, num_keywords=10))
    
    # Scenario 2: Medium text, medium keywords
    results.append(run_benchmark(text_size=10_000, num_keywords=50))
    
    # Scenario 3: Large text, many keywords
    results.append(run_benchmark(text_size=100_000, num_keywords=500))
    
    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    print(f"{'Scenario':<30} {'Speedup'}")
    print("-"*60)
    
    scenarios = [
        "Small (1k words, 10 keywords)",
        "Medium (10k words, 50 keywords)",
        "Large (100k words, 500 keywords)"
    ]
    
    for scenario, result in zip(scenarios, results):
        print(f"{scenario:<30} {result['speedup']:.1f}x")
    
    avg_speedup = sum(r['speedup'] for r in results) / len(results)
    print(f"\n{'Average speedup:':<30} {avg_speedup:.1f}x")
    print(f"{'='*60}")
    
    # Recommendation
    print("\n RECOMMENDATION:")
    print("   Use FlashText when:")
    print("   - You have 50+ keywords")
    print("   - Processing large text volumes")
    print("   - Exact matches work (no regex patterns needed)")
    print("\n   Use Regex when:")
    print("   - You have <10 keywords")
    print("   - You need pattern matching (wildcards, lookaheads)")
    print("   - Small text volumes")


if __name__ == '__main__':
    main()
