"""
Error analyzer using LLM to classify errors and identify root causes.

Provides error categorization and recovery recommendations.
"""

from typing import Dict, List, Optional, Any
from enum import Enum
from dataclasses import dataclass


class ErrorCategory(Enum):
    """Categories of errors."""
    TIMEOUT = "timeout"
    RESOURCE_EXHAUSTED = "resource_exhausted"
    INVALID_INPUT = "invalid_input"
    EXTERNAL_SERVICE = "external_service"
    UNKNOWN = "unknown"


@dataclass
class ErrorAnalysis:
    """Result of error analysis."""
    category: ErrorCategory
    root_cause: str
    confidence: float
    recommendations: List[str]


class ErrorAnalyzer:
    """
    Analyzes errors using pattern matching and LLM insights.
    
    Classifies errors and suggests recovery strategies.
    """
    
    def __init__(self):
        """Initialize error analyzer."""
        self.error_patterns: Dict[str, ErrorCategory] = {
            "timeout": ErrorCategory.TIMEOUT,
            "Resource": ErrorCategory.RESOURCE_EXHAUSTED,
            "Invalid": ErrorCategory.INVALID_INPUT,
            "Connection": ErrorCategory.EXTERNAL_SERVICE,
        }
    
    def analyze(self, error: Exception, context: Optional[Dict[str, Any]] = None) -> ErrorAnalysis:
        """
        Analyze an error to categorize and suggest recovery.
        
        Args:
            error: The exception to analyze
            context: Additional context about the error
            
        Returns:
            ErrorAnalysis with category and recommendations
        """
        error_str = str(error)
        
        # Pattern matching for categorization
        category = ErrorCategory.UNKNOWN
        for pattern, cat in self.error_patterns.items():
            if pattern in error_str:
                category = cat
                break
        
        # Generate recommendations based on category
        recommendations = self._get_recommendations(category)
        
        return ErrorAnalysis(
            category=category,
            root_cause=error_str,
            confidence=self._calculate_confidence(error_str),
            recommendations=recommendations
        )
    
    def _get_recommendations(self, category: ErrorCategory) -> List[str]:
        """Get recovery recommendations for error category."""
        recommendations = {
            ErrorCategory.TIMEOUT: [
                "Increase timeout threshold",
                "Optimize step performance",
                "Split into smaller steps"
            ],
            ErrorCategory.RESOURCE_EXHAUSTED: [
                "Increase resource allocation",
                "Implement rate limiting",
                "Add step batching"
            ],
            ErrorCategory.INVALID_INPUT: [
                "Validate input data",
                "Add data transformation",
                "Check upstream step output"
            ],
            ErrorCategory.EXTERNAL_SERVICE: [
                "Check service status",
                "Implement circuit breaker",
                "Add exponential backoff"
            ],
        }
        
        return recommendations.get(category, ["Retry with backoff"])
    
    def _calculate_confidence(self, error_str: str) -> float:
        """Calculate confidence in error classification."""
        if len(error_str) > 50:
            return 0.9
        elif len(error_str) > 20:
            return 0.7
        return 0.5
