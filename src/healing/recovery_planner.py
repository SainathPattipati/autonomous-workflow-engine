"""
Recovery planner that generates fix strategies for errors.

Plans retry strategies, fallbacks, and escalation logic.
"""

from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass
from enum import Enum


class RecoveryStrategy(Enum):
    """Recovery strategies for errors."""
    RETRY = "retry"
    FALLBACK = "fallback"
    SKIP = "skip"
    ESCALATE = "escalate"


@dataclass
class RecoveryPlan:
    """Represents a recovery plan for an error."""
    strategy: RecoveryStrategy
    steps: List[str]
    max_attempts: int
    escalation_enabled: bool


class RecoveryPlanner:
    """
    Plans recovery strategies for detected errors.
    
    Generates retry plans, fallback paths, and escalation triggers.
    """
    
    def __init__(self):
        """Initialize recovery planner."""
        self.fallback_tasks: Dict[str, Callable] = {}
    
    def plan_recovery(
        self,
        step_name: str,
        error_category: str,
        context: Optional[Dict[str, Any]] = None
    ) -> RecoveryPlan:
        """
        Plan recovery for a failed step.
        
        Args:
            step_name: Name of failed step
            error_category: Category of error
            context: Additional context
            
        Returns:
            RecoveryPlan with strategy and steps
        """
        context = context or {}
        
        if error_category == "timeout":
            return RecoveryPlan(
                strategy=RecoveryStrategy.RETRY,
                steps=[
                    f"Increase timeout for {step_name}",
                    f"Retry {step_name} with backoff"
                ],
                max_attempts=3,
                escalation_enabled=True
            )
        elif error_category == "resource_exhausted":
            return RecoveryPlan(
                strategy=RecoveryStrategy.RETRY,
                steps=[
                    f"Wait for resource availability",
                    f"Retry {step_name}"
                ],
                max_attempts=5,
                escalation_enabled=False
            )
        elif error_category == "invalid_input":
            return RecoveryPlan(
                strategy=RecoveryStrategy.SKIP,
                steps=[
                    f"Validate input for {step_name}",
                    f"Skip {step_name} or use default"
                ],
                max_attempts=1,
                escalation_enabled=True
            )
        else:
            return RecoveryPlan(
                strategy=RecoveryStrategy.ESCALATE,
                steps=["Notify administrator"],
                max_attempts=0,
                escalation_enabled=True
            )
    
    def register_fallback(self, step_name: str, fallback: Callable) -> None:
        """
        Register a fallback function for a step.
        
        Args:
            step_name: Step name
            fallback: Fallback function to execute
        """
        self.fallback_tasks[step_name] = fallback
    
    def execute_fallback(self, step_name: str) -> Optional[Any]:
        """
        Execute fallback for a step.
        
        Args:
            step_name: Step name
            
        Returns:
            Fallback result or None
        """
        if step_name in self.fallback_tasks:
            return self.fallback_tasks[step_name]()
        return None
