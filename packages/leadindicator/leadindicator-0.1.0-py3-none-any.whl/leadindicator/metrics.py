"""
Metrics and statistical calculations for threshold analysis.
"""

from dataclasses import dataclass
from typing import Optional

@dataclass
class ThresholdMetrics:
    """Container for threshold analysis metrics."""
    
    threshold: float
    sensitivity: float  # Capture rate
    specificity: float
    precision: float
    f1_score: float
    event_probability: float
    avg_severity: float
    affected_categories: Optional[int]
    n_observations: int
    capture_rate: float
    true_positives: int
    false_positives: int
    true_negatives: int
    false_negatives: int
    
    @property
    def balanced_accuracy(self) -> float:
        """Calculate balanced accuracy (mean of sensitivity and specificity)."""
        return (self.sensitivity + self.specificity) / 2
    
    @property
    def balanced_score(self) -> float:
        """Calculate balanced score (mean of sensitivity, specificity, and F1)."""
        return (self.sensitivity + self.specificity + self.f1_score) / 3
    
    def to_dict(self) -> dict:
        """Convert metrics to dictionary."""
        return {
            "threshold": self.threshold,
            "sensitivity": self.sensitivity,
            "specificity": self.specificity,
            "precision": self.precision,
            "f1_score": self.f1_score,
            "event_probability": self.event_probability,
            "avg_severity": self.avg_severity,
            "affected_categories": self.affected_categories,
            "n_observations": self.n_observations,
            "capture_rate": self.capture_rate,
            "true_positives": self.true_positives,
            "false_positives": self.false_positives,
            "true_negatives": self.true_negatives,
            "false_negatives": self.false_negatives,
            "balanced_accuracy": self.balanced_accuracy,
            "balanced_score": self.balanced_score
        }
    
    def __str__(self) -> str:
        """Human-readable string representation."""
        return (
            f"Threshold ≥ {self.threshold:.2f}\n"
            f"  Sensitivity: {self.sensitivity:.1f}%\n"
            f"  Specificity: {self.specificity:.1f}%\n"
            f"  Precision: {self.precision:.1f}%\n"
            f"  F1 Score: {self.f1_score:.1f}%\n"
            f"  Event Probability: {self.event_probability:.1f}%\n"
            f"  Observations: {self.n_observations}"
        ) 