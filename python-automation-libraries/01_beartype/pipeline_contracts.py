"""
01_beartype/pipeline_contracts.py
-----------------------------------
Real-world pattern: using @beartype as a contract enforcer across
data pipeline stages. Each stage declares its input/output types,
and Beartype validates them at runtime — catching dirty data early.
"""

from beartype import beartype
from dataclasses import dataclass


#  Data models
@dataclass
class RawRecord:
    source: str
    payload: dict


@dataclass
class CleanRecord:
    id: int
    name: str
    value: float


@dataclass
class EnrichedRecord:
    id: int
    name: str
    value: float
    category: str
    flagged: bool


#  Pipeline stages — each enforced by @beartype
@beartype
def ingest(raw: dict) -> RawRecord:
    """Stage 1: Wrap raw dict into a typed RawRecord."""
    if "source" not in raw or "payload" not in raw:
        raise ValueError("Raw data must have 'source' and 'payload' keys.")
    return RawRecord(source=raw["source"], payload=raw["payload"])


@beartype
def clean(record: RawRecord) -> CleanRecord:
    """Stage 2: Validate and coerce fields from the raw payload."""
    payload = record.payload
    return CleanRecord(
        id=int(payload["id"]),
        name=str(payload["name"]).strip().title(),
        value=float(payload["value"]),
    )


@beartype
def enrich(record: CleanRecord, categories: dict[int, str]) -> EnrichedRecord:
    """Stage 3: Enrich with category lookup and flag high-value records."""
    return EnrichedRecord(
        id=record.id,
        name=record.name,
        value=record.value,
        category=categories.get(record.id, "unknown"),
        flagged=record.value > 1000.0,
    )


@beartype
def export(record: EnrichedRecord) -> dict:
    """Stage 4: Serialize to dict for downstream storage."""
    return {
        "id": record.id,
        "name": record.name,
        "value": record.value,
        "category": record.category,
        "flagged": record.flagged,
    }


#  Pipeline runner
def run_pipeline(raw_inputs: list[dict], category_map: dict[int, str]) -> list[dict]:
    """Runs all four pipeline stages for each raw input record."""
    results = []
    for raw in raw_inputs:
        try:
            stage1 = ingest(raw)
            stage2 = clean(stage1)
            stage3 = enrich(stage2, category_map)
            stage4 = export(stage3)
            results.append(stage4)
        except Exception as e:
            print(f"  ⚠ Skipped record {raw} — {type(e).__name__}: {e}")
    return results


#  Demo 

if __name__ == "__main__":
    print("=" * 55)
    print("BEARTYPE — Pipeline Contracts Example")
    print("=" * 55)

    sample_inputs = [
        {"source": "api_v2", "payload": {"id": "101", "name": "  widget pro  ", "value": "249.99"}},
        {"source": "csv_import", "payload": {"id": "202", "name": "PREMIUM BUNDLE", "value": "1500.00"}},
        # Dirty record — missing value field
        {"source": "manual", "payload": {"id": "303", "name": "Sample"}},
    ]

    categories = {101: "hardware", 202: "software"}

    print("\nRunning pipeline...\n")
    output = run_pipeline(sample_inputs, categories)

    print("\n Pipeline output:\n")
    for record in output:
        flagged = "FLAGGED" if record["flagged"] else "✓"
        print(f"  {flagged} {record}")
