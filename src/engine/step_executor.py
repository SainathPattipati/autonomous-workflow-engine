"""
Step executor with retry logic and timeout handling.

Executes individual steps with exponential backoff and validation.
"""

from typing import Any, Optional, Callable, Dict
import asyncio
import time


class StepExecutor:
    """
    Executes workflow steps with retry logic and timeout handling.
    
    Supports parallel execution and result validation.
    """
    
    def __init__(self, max_retries: int = 3, base_timeout: float = 30.0):
        """
        Initialize step executor.
        
        Args:
            max_retries: Maximum retry attempts
            base_timeout: Base timeout in seconds
        """
        self.max_retries = max_retries
        self.base_timeout = base_timeout
        self.execution_metrics: Dict[str, Dict[str, Any]] = {}
    
    async def execute(
        self,
        step_name: str,
        task: Callable,
        validate: Optional[Callable[[Any], bool]] = None
    ) -> Optional[Any]:
        """
        Execute step with retry logic.
        
        Args:
            step_name: Name of the step
            task: Async function to execute
            validate: Optional validation function
            
        Returns:
            Result or None if all retries exhausted
        """
        self.execution_metrics[step_name] = {
            "attempts": 0,
            "start_time": time.time(),
            "success": False
        }
        
        for attempt in range(self.max_retries):
            self.execution_metrics[step_name]["attempts"] = attempt + 1
            
            try:
                # Execute with timeout
                result = await asyncio.wait_for(
                    task(),
                    timeout=self.base_timeout
                )
                
                # Validate result if validator provided
                if validate and not validate(result):
                    raise ValueError("Result validation failed")
                
                self.execution_metrics[step_name]["success"] = True
                self.execution_metrics[step_name]["duration"] = (
                    time.time() - self.execution_metrics[step_name]["start_time"]
                )
                
                return result
            
            except asyncio.TimeoutError:
                if attempt < self.max_retries - 1:
                    backoff = 2 ** attempt
                    await asyncio.sleep(backoff)
            except Exception as e:
                if attempt < self.max_retries - 1:
                    backoff = 2 ** attempt
                    await asyncio.sleep(backoff)
                else:
                    raise
        
        return None
    
    def get_metrics(self, step_name: str) -> Dict[str, Any]:
        """Get execution metrics for a step."""
        return self.execution_metrics.get(step_name, {})
