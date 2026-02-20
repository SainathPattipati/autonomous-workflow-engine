"""Example: Data pipeline workflow with error recovery."""

from typing import Dict, Any

def example_data_pipeline() -> Dict[str, Any]:
    """Define a data pipeline workflow."""
    return {
        "name": "data_pipeline",
        "description": "End-to-end data processing pipeline",
        "steps": [
            {"name": "extract", "depends_on": [], "timeout": 60},
            {"name": "validate", "depends_on": ["extract"], "timeout": 30},
            {"name": "transform", "depends_on": ["validate"], "timeout": 120},
            {"name": "aggregate", "depends_on": ["transform"], "timeout": 60},
            {"name": "load", "depends_on": ["aggregate"], "timeout": 90}
        ]
    }

if __name__ == "__main__":
    pipeline = example_data_pipeline()
    print(f"Pipeline: {pipeline['name']}")
    print(f"Steps: {len(pipeline['steps'])}")
