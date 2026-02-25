"""
01_beartype/advanced_generics.py
----------------------------------
Advanced Beartype: Union types, TypedDict, Callable type hints,
and class-level enforcement using BeartypeConf for global configuration.
"""

from beartype import beartype, BeartypeConf
from beartype.typing import Union, Callable, TypedDict


#  TypedDict - Beartype validates structure of dicts -
class JobConfig(TypedDict):
    job_id: str
    retries: int
    timeout: float


@beartype
def schedule_job(config: JobConfig) -> str:
    return f"Scheduled job {config['job_id']} with {config['retries']} retries."


#  Union types -
@beartype
def parse_identifier(value: Union[int, str]) -> str:
    """Accepts either an int or str identifier and normalizes to str."""
    return str(value).strip().lower()


#  Callable type hints -
@beartype
def apply_transform(
    data: list[float],
    transform: Callable[[float], float]
) -> list[float]:
    """Applies a callable transform to each item. Beartype checks the callable signature."""
    return [transform(x) for x in data]


#  Class-level Beartype with BeartypeConf
beartype_strict = beartype(conf=BeartypeConf(is_debug=False))


class DataNormalizer:
    """All public methods are type-checked via @beartype_strict decorator."""

    @beartype_strict
    def normalize(self, values: list[float], scale: float = 1.0) -> list[float]:
        max_val = max(values) if values else 1.0
        return [(v / max_val) * scale for v in values]

    @beartype_strict
    def clip(self, values: list[float], low: float, high: float) -> list[float]:
        return [max(low, min(high, v)) for v in values]


#  Demo 

if __name__ == "__main__":
    print("=" * 55)
    print("BEARTYPE - Advanced Generics Examples")
    print("=" * 55)

    # TypedDict
    print("\n TypedDict ")
    config: JobConfig = {"job_id": "etl-001", "retries": 3, "timeout": 30.0}
    print(schedule_job(config))

    # Union
    print("\n Union Types ")
    print(parse_identifier(42))
    print(parse_identifier("  JOB-99  "))

    # Callable
    print("\n Callable Type Hints ")
    doubled = apply_transform([1.0, 2.5, 3.0], lambda x: x * 2)
    print(f"Doubled: {doubled}")

    # Class-level
    print("\n Class-Level Beartype ")
    normalizer = DataNormalizer()
    raw = [10.0, 25.0, 50.0, 100.0]
    normalized = normalizer.normalize(raw, scale=100.0)
    clipped = normalizer.clip(normalized, low=20.0, high=80.0)
    print(f"Normalized: {normalized}")
    print(f"Clipped:    {clipped}")

    # Type violation
    print("\n Violation caught ")
    try:
        schedule_job({"job_id": 123, "retries": "three", "timeout": 30.0})  # type: ignore
    except Exception as e:
        print(f"{type(e).__name__} raised - type contract enforced ✓")
