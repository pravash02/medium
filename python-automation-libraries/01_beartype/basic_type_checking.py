"""
01_beartype/basic_type_checking.py
-----------------------------------
Basic Beartype usage: decorating functions with @beartype to enforce
type hints at runtime. Demonstrates how Beartype catches type violations
that mypy would miss at runtime.
"""

from beartype import beartype
from beartype.typing import Optional


#  Example 1: Simple function with type enforcement
@beartype
def greet_user(name: str, age: int) -> str:
    """Returns a greeting string. Both args are type-checked at call time."""
    return f"Hello, {name}! You are {age} years old."


#  Example 2: Optional types
@beartype
def process_record(
    record_id: int,
    label: str,
    description: Optional[str] = None
) -> dict:
    """Processes a record. description is optional but must be str if provided."""
    return {
        "id": record_id,
        "label": label,
        "description": description or "N/A",
    }


#  Example 3: Nested types
@beartype
def sum_scores(scores: list[int]) -> int:
    """Expects a list of integers. Beartype validates the container type."""
    return sum(scores)


#  Runner
def run_demos():
    print("=" * 55)
    print("BEARTYPE — Basic Type Checking Examples")
    print("=" * 55)

    # Valid calls
    print("\n Valid calls:\n")

    result = greet_user("Alice", 30)
    print(f"greet_user('Alice', 30)         → {result}")

    record = process_record(42, "invoice", "Q4 report")
    print(f"process_record(42, 'invoice')   → {record}")

    total = sum_scores([10, 20, 30])
    print(f"sum_scores([10, 20, 30])        → {total}")

    # Invalid calls — Beartype raises BeartypeException
    print("\n Invalid calls (Beartype catches these):\n")

    invalid_calls = [
        ("greet_user('Alice', '30')",    lambda: greet_user("Alice", "30")),
        ("process_record('abc', 'lbl')", lambda: process_record("abc", "label")),
        ("sum_scores([1, 'two', 3])",    lambda: sum_scores([1, "two", 3])),
    ]

    for label, fn in invalid_calls:
        try:
            fn()
        except Exception as e:
            # Show just the exception type and first line of the message
            first_line = str(e).split("\n")[0][:80]
            print(f"  {label}")
            print(f"  → {type(e).__name__}: {first_line}...\n")


if __name__ == "__main__":
    run_demos()
