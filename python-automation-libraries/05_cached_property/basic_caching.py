"""
05_cached_property/basic_caching.py  &  config_pattern.py
------------------------------------------------------------
Demonstrates functools.cached_property for expensive computations
that should only run once per instance lifetime.
"""

import time
import json
import os
import tempfile
from functools import cached_property


# =======================================================
# PART 1: Basic Caching — Performance Comparison
# =======================================================

class WithoutCache:
    """Naive approach: expensive computation runs on every access."""

    @property
    def heavy_analysis(self) -> dict:
        time.sleep(0.3)  # Simulate expensive work
        return {"status": "computed", "count": 42}


class WithCache:
    """Optimized: expensive computation runs exactly once."""

    @cached_property
    def heavy_analysis(self) -> dict:
        time.sleep(0.3)  # Runs ONCE, then cached in __dict__
        return {"status": "computed", "count": 42}


def demo_performance_comparison():
    print("=" * 55)
    print("CACHED_PROPERTY — Performance Comparison")
    print("=" * 55)

    ACCESSES = 5

    # Without cache
    obj = WithoutCache()
    start = time.perf_counter()
    for _ in range(ACCESSES):
        _ = obj.heavy_analysis
    without_time = time.perf_counter() - start

    # With cache
    obj_cached = WithCache()
    start = time.perf_counter()
    for _ in range(ACCESSES):
        _ = obj_cached.heavy_analysis
    with_time = time.perf_counter() - start

    print(f"\n  {ACCESSES} accesses WITHOUT cached_property: {without_time:.3f}s")
    print(f"  {ACCESSES} accesses WITH    cached_property: {with_time:.3f}s")
    print(f"  Speedup: {without_time / with_time:.1f}x faster\n")

    # Verify it's actually cached (stored in __dict__)
    print(f"  obj_cached.__dict__ keys: {list(obj_cached.__dict__.keys())}")
    print(" Result stored directly on instance — zero overhead after first call")


# =======================================================
# PART 2: Real-World Config Pattern
# =======================================================

class PipelineConfig:
    """
    Configuration loader for an automation pipeline.
    Uses cached_property so config files, parsed schemas, and
    derived settings are read/computed once and reused throughout.
    """

    def __init__(self, config_path: str):
        self.config_path = config_path

    @cached_property
    def raw_config(self) -> dict:
        """Read and parse config file — runs once per instance."""
        print(f"  [IO] Reading config from {self.config_path}...")
        with open(self.config_path) as f:
            return json.load(f)

    @cached_property
    def database_url(self) -> str:
        """Derived setting — computed from raw_config once."""
        db = self.raw_config.get("database", {})
        return f"{db['driver']}://{db['host']}:{db['port']}/{db['name']}"

    @cached_property
    def allowed_sources(self) -> set[str]:
        """Normalize sources to a set for O(1) lookup."""
        return set(self.raw_config.get("sources", []))

    @cached_property
    def feature_flags(self) -> dict[str, bool]:
        """Parse and validate feature flags."""
        flags = self.raw_config.get("features", {})
        return {k: bool(v) for k, v in flags.items()}

    def invalidate_cache(self):
        """Force re-read of config (e.g., after config file changes)."""
        for attr in ["raw_config", "database_url", "allowed_sources", "feature_flags"]:
            self.__dict__.pop(attr, None)
        print("  [cache] Invalidated — next access will re-read from disk.")


def demo_config_pattern():
    print("\n" + "=" * 55)
    print("CACHED_PROPERTY — Config Pattern")
    print("=" * 55)

    # Create a temp config file
    config_data = {
        "database": {"driver": "postgresql", "host": "db.internal", "port": 5432, "name": "automation"},
        "sources": ["api_v1", "api_v2", "csv_feed", "webhook"],
        "features": {"dry_run": False, "verbose_logging": True, "parallel_fetch": True},
    }
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump(config_data, f)
        config_path = f.name

    try:
        config = PipelineConfig(config_path)

        print(f"\n  First access (triggers file read):")
        print(f"  database_url:     {config.database_url}")

        print(f"\n  Subsequent accesses (from cache — no file read):")
        print(f"  database_url:     {config.database_url}")
        print(f"  allowed_sources:  {config.allowed_sources}")
        print(f"  feature_flags:    {config.feature_flags}")

        print(f"\n  Source check ('api_v1' allowed?): {'api_v1' in config.allowed_sources}")
        print(f"  Source check ('rss_feed' allowed?): {'rss_feed' in config.allowed_sources}")

        # Invalidation demo
        print(f"\n  Invalidating cache...")
        config.invalidate_cache()
        print(f"  Re-accessing database_url (re-reads file):")
        print(f"  {config.database_url}")

    finally:
        os.unlink(config_path)

    print("\n cached_property — zero external dependencies, maximum impact.")


# =======================================================
# PART 3: Thread-Safe Variant
# =======================================================

import threading

class ThreadSafeConfig:
    """
    For multi-threaded automation workers, protect first-compute
    with a lock. After initialization, all reads are lock-free.
    """

    def __init__(self):
        self._lock = threading.Lock()

    @cached_property
    def expensive_resource(self) -> dict:
        with self._lock:
            # Double-check inside lock (thread-safe initialization pattern)
            if "expensive_resource" in self.__dict__:
                return self.__dict__["expensive_resource"]
            time.sleep(0.1)  # Simulate expensive setup
            return {"connection_pool": "initialized", "max_connections": 20}


if __name__ == "__main__":
    demo_performance_comparison()
    demo_config_pattern()

    print("\n" + "=" * 55)
    print("CACHED_PROPERTY — Thread-Safe Variant")
    print("=" * 55)
    ts = ThreadSafeConfig()
    threads = [threading.Thread(target=lambda: ts.expensive_resource) for _ in range(5)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print(f"\n  Resource (accessed from 5 threads): {ts.expensive_resource}")
    print("  Computed once, safely shared across threads.")
