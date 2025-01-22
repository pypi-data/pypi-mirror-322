"""
LeadIndicator - A package for analyzing leading indicators and finding optimal thresholds.
"""

from .analyzer import ThresholdAnalyzer, AnalyzerConfig
from .metrics import ThresholdMetrics
from .visualization import plot_threshold_analysis

__version__ = "0.1.0"

__all__ = [
    "ThresholdAnalyzer",
    "AnalyzerConfig",
    "ThresholdMetrics",
    "plot_threshold_analysis",
] 