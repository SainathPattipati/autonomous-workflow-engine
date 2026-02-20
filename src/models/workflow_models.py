"""Pydantic models for workflow definition and execution."""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class StepModel(BaseModel):
    """Step definition model."""
    name: str
    depends_on: List[str] = Field(default_factory=list)
    timeout: float = 30.0
    retries: int = 3
    description: Optional[str] = None


class WorkflowModel(BaseModel):
    """Workflow definition model."""
    name: str
    steps: List[StepModel]
    description: Optional[str] = None
    version: str = "1.0.0"


class ExecutionResultModel(BaseModel):
    """Execution result model."""
    execution_id: str
    workflow_name: str
    status: str
    results: Dict[str, Any] = Field(default_factory=dict)
    errors: Dict[str, str] = Field(default_factory=dict)
    started_at: str
    completed_at: Optional[str] = None
