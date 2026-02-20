# Autonomous Workflow Engine

**Self-healing workflow automation with AI-powered error recovery**

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview

Production-grade workflow automation engine with self-healing capabilities. Detects errors, analyzes root causes, and automatically plans recovery strategies.

## Key Features

- **DAG-based workflows** with dependency resolution
- **Async execution** with state persistence
- **AI-powered error analysis** using LLM
- **Self-healing recovery** with exponential backoff
- **Timeout handling** and circuit breaker patterns
- **Parallel step execution** where possible
- **Human escalation** for unrecoverable errors

## Quick Start

```bash
pip install autonomous-workflow-engine
```

### Example

```python
from engine import WorkflowEngine, WorkflowDefinition

engine = WorkflowEngine()

# Define workflow
workflow = WorkflowDefinition(
    name="data_pipeline",
    steps=[
        {"name": "extract", "depends_on": []},
        {"name": "transform", "depends_on": ["extract"]},
        {"name": "validate", "depends_on": ["transform"]},
        {"name": "load", "depends_on": ["validate"]}
    ]
)

# Execute with self-healing
result = engine.execute(workflow)
```

## Architecture

### WorkflowEngine
Manages DAG execution and state persistence.

### StepExecutor
Executes individual steps with timeout and retry logic.

### ErrorAnalyzer
Uses LLM to classify and understand errors.

### RecoveryPlanner
Generates recovery strategies for detected errors.

## Contributing

See CONTRIBUTING.md

## License

MIT License
