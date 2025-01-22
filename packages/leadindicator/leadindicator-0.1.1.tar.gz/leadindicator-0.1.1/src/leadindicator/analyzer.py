"""
Core analyzer class for threshold analysis.
"""

import polars as pl
from typing import List, Optional, Dict, Union
from dataclasses import dataclass
from pathlib import Path
import os

from .metrics import ThresholdMetrics
from .visualization import create_visualizations
from .report import generate_report

@dataclass
class AnalyzerConfig:
    """Configuration for threshold analysis."""
    score_column: str
    target_column: str
    category_column: Optional[str] = None
    min_capture_rate: float = 30.0
    min_specificity: float = 50.0
    percentile_thresholds: List[float] = None
    min_threshold_spacing: float = 0.1  # Minimum spacing between thresholds as fraction of range
    fallback_percentiles: List[float] = None  # Percentiles to use if optimal thresholds not found
    
    def __post_init__(self):
        """Validate configuration and set defaults."""
        if self.percentile_thresholds is None:
            self.percentile_thresholds = [0.5, 0.75, 0.9]
            
        if self.fallback_percentiles is None:
            self.fallback_percentiles = [0.6, 0.75, 0.9]  # Warning, High Risk, Critical
        
        # Convert any integer percentiles to float
        self.percentile_thresholds = [p/100 if p > 1 else p for p in self.percentile_thresholds]
        self.fallback_percentiles = [p/100 if p > 1 else p for p in self.fallback_percentiles]
        
        # Validate percentiles
        if not all(0 <= p <= 1 for p in self.percentile_thresholds):
            raise ValueError("Percentiles must be between 0 and 1")
        if not all(0 <= p <= 1 for p in self.fallback_percentiles):
            raise ValueError("Fallback percentiles must be between 0 and 1")
        
        # Validate rates and spacing
        if not (0 <= self.min_capture_rate <= 100):
            raise ValueError("min_capture_rate must be between 0 and 100")
        if not (0 <= self.min_specificity <= 100):
            raise ValueError("min_specificity must be between 0 and 100")
        if not (0 < self.min_threshold_spacing < 1):
            raise ValueError("min_threshold_spacing must be between 0 and 1")

class ThresholdAnalyzer:
    """
    Analyzer for finding optimal thresholds in leading indicators.
    
    The analyzer uses a multi-step process to find optimal thresholds:
    1. Identifies all thresholds that meet minimum criteria (capture rate and specificity)
    2. Ranks thresholds by a balanced score (sensitivity + specificity + F1)
    3. Ensures meaningful spacing between selected thresholds
    4. Falls back to percentile-based thresholds if optimal ones can't be found
    
    Example:
        >>> analyzer = ThresholdAnalyzer(
        ...     score_column="Risk Score",
        ...     target_column="Event Count",
        ...     category_column="Category",
        ...     min_capture_rate=30.0,
        ...     min_specificity=50.0,
        ...     min_threshold_spacing=0.1,
        ...     fallback_percentiles=[60, 75, 90]
        ... )
        >>> results = analyzer.analyze("data.csv")
        >>> results.save_report("analysis.html")
    """
    
    def __init__(
        self,
        score_column: str,
        target_column: str,
        category_column: Optional[str] = None,
        min_capture_rate: float = 30.0,
        min_specificity: float = 50.0,
        percentile_thresholds: Optional[List[float]] = None,
        min_threshold_spacing: float = 0.1,
        fallback_percentiles: Optional[List[float]] = None
    ):
        """Initialize the analyzer with configuration.
        
        Args:
            score_column: Name of the column containing the leading indicator scores
            target_column: Name of the column containing the target events
            category_column: Optional name of the column for categorical analysis
            min_capture_rate: Minimum percentage of events to capture (sensitivity)
            min_specificity: Minimum percentage of non-events to exclude
            percentile_thresholds: List of percentiles to try as initial thresholds
            min_threshold_spacing: Minimum spacing between thresholds as fraction of range
            fallback_percentiles: Percentiles to use if optimal thresholds not found
        """
        self.config = AnalyzerConfig(
            score_column=score_column,
            target_column=target_column,
            category_column=category_column,
            min_capture_rate=min_capture_rate,
            min_specificity=min_specificity,
            percentile_thresholds=percentile_thresholds,
            min_threshold_spacing=min_threshold_spacing,
            fallback_percentiles=fallback_percentiles
        )
        self.df = None
        self.results = None
        self.category_patterns = None
    
    def load_data(self, file_path: Union[str, Path]) -> None:
        """Load data from file."""
        file_path = str(file_path)
        try:
            if file_path.endswith('.xlsx'):
                self.df = pl.read_excel(file_path)
            elif file_path.endswith('.csv'):
                self.df = pl.read_csv(file_path)
            else:
                raise ValueError("Unsupported file format. Use .xlsx or .csv")
        except Exception as e:
            raise IOError(f"Error loading data from {file_path}: {str(e)}")
        
        self._validate_data()
    
    def _validate_data(self) -> None:
        """Validate loaded data."""
        if self.df is None:
            raise ValueError("No data loaded. Call load_data() first.")
            
        if self.df.is_empty():
            raise ValueError("Dataset is empty")
            
        required_columns = [self.config.score_column, self.config.target_column]
        if self.config.category_column:
            required_columns.append(self.config.category_column)
            
        missing_cols = [col for col in required_columns if col not in self.df.columns]
        if missing_cols:
            raise ValueError(f"Missing required columns: {missing_cols}")
            
        # Check for negative event counts
        if (self.df[self.config.target_column] < 0).any():
            raise ValueError("Negative event counts found in data")
    
    def analyze_categories(self) -> Optional[pl.DataFrame]:
        """Analyze patterns by category."""
        if not self.config.category_column:
            return None
            
        self.category_patterns = self.df.group_by(self.config.category_column).agg([
            pl.col(self.config.target_column).mean().alias("avg_event_rate"),
            pl.col(self.config.score_column).mean().alias("avg_score"),
            pl.count().alias("n_observations"),
            (pl.col(self.config.target_column) > 0).sum().alias("n_events"),
            pl.col(self.config.target_column).sum().alias("total_events"),
            pl.col(self.config.target_column).max().alias("max_events")
        ])
        
        return self.category_patterns
    
    def calculate_threshold_metrics(self, threshold: float) -> ThresholdMetrics:
        """Calculate metrics for a specific threshold."""
        above = self.df.filter(pl.col(self.config.score_column) >= threshold)
        below = self.df.filter(pl.col(self.config.score_column) < threshold)
        
        total_events = (self.df[self.config.target_column] > 0).sum()
        above_events = (above[self.config.target_column] > 0).sum()
        
        # Basic counts
        true_positives = above_events
        false_positives = len(above) - above_events
        false_negatives = total_events - above_events
        true_negatives = len(below) - (total_events - above_events)
        
        # Calculate metrics
        sensitivity = (true_positives / total_events * 100) if total_events > 0 else 0
        specificity = (true_negatives / (true_negatives + false_positives) * 100) if (true_negatives + false_positives) > 0 else 0
        precision = (true_positives / (true_positives + false_positives) * 100) if (true_positives + false_positives) > 0 else 0
        
        # F1 score
        recall = sensitivity / 100
        prec = precision / 100
        f1_score = 2 * (prec * recall) / (prec + recall) if (prec + recall) > 0 else 0
        
        # Other metrics
        event_prob = (above_events / len(above) * 100) if len(above) > 0 else 0
        avg_severity = above.select(pl.col(self.config.target_column).mean()).item()
        affected_cats = len(above.select(self.config.category_column).unique()) if self.config.category_column else None
        
        return ThresholdMetrics(
            threshold=threshold,
            sensitivity=sensitivity,
            specificity=specificity,
            precision=precision,
            f1_score=f1_score * 100,
            event_probability=event_prob,
            avg_severity=avg_severity,
            affected_categories=affected_cats,
            n_observations=len(above),
            capture_rate=sensitivity,
            true_positives=true_positives,
            false_positives=false_positives,
            true_negatives=true_negatives,
            false_negatives=false_negatives
        )
    
    def find_optimal_thresholds(self) -> List[float]:
        """
        Find optimal thresholds using comprehensive search.
        
        The process follows these steps:
        1. Calculate metrics for all unique score values
        2. Filter thresholds that meet minimum criteria
        3. Sort by balanced performance score
        4. Select thresholds with meaningful spacing
        5. Fall back to percentile-based approach if needed
        
        Returns:
            List[float]: Three thresholds for Warning, High Risk, and Critical levels
        """
        # If percentile thresholds are specified, use them directly
        if self.config.percentile_thresholds:
            return [
                self.df.select(pl.col(self.config.score_column).quantile(p)).item()
                for p in self.config.percentile_thresholds
            ]
            
        # Otherwise, proceed with optimal threshold search
        unique_scores = sorted(self.df[self.config.score_column].unique().to_list())
        
        # Calculate metrics for each threshold
        threshold_metrics = []
        for threshold in unique_scores:
            metrics = self.calculate_threshold_metrics(threshold)
            if (metrics.sensitivity >= self.config.min_capture_rate and 
                metrics.specificity >= self.config.min_specificity):
                threshold_metrics.append((threshold, metrics))
        
        if not threshold_metrics:
            print("Warning: No thresholds meet minimum criteria. Using fallback percentiles.")
            return [
                self.df.select(pl.col(self.config.score_column).quantile(p)).item()
                for p in self.config.fallback_percentiles
            ]
        
        # Sort by balanced score
        sorted_thresholds = sorted(
            threshold_metrics,
            key=lambda x: (x[1].sensitivity + x[1].specificity + x[1].f1_score) / 3,
            reverse=True
        )
        
        # Get the range of valid thresholds
        min_threshold = min(t[0] for t in threshold_metrics)
        max_threshold = max(t[0] for t in threshold_metrics)
        threshold_range = max_threshold - min_threshold
        
        # Ensure meaningful spacing between thresholds
        min_spacing = threshold_range * self.config.min_threshold_spacing
        selected_thresholds = []
        
        for threshold, metrics in sorted_thresholds:
            if not selected_thresholds or (threshold - selected_thresholds[-1]) >= min_spacing:
                selected_thresholds.append(threshold)
                if len(selected_thresholds) == 3:
                    break
        
        # If we couldn't find enough spaced thresholds, use fallback percentiles
        if len(selected_thresholds) < 3:
            print("Warning: Could not find enough spaced thresholds. Using fallback percentiles.")
            selected_thresholds = [
                self.df.select(pl.col(self.config.score_column).quantile(p)).item()
                for p in self.config.fallback_percentiles
            ]
        
        return selected_thresholds
    
    def analyze(self, data: Union[str, Path, pl.DataFrame, 'pd.DataFrame']) -> 'AnalysisResults':
        """Run complete analysis pipeline.
        
        Args:
            data: Can be:
                - Path to a CSV or Excel file
                - polars DataFrame
                - pandas DataFrame
        """
        # Load data if path provided
        if isinstance(data, (str, Path)):
            self.load_data(data)
        else:
            # Convert pandas DataFrame to polars if needed
            if 'pandas' in str(type(data)):
                self.df = pl.from_pandas(data)
            else:
                self.df = data
        
        self._validate_data()
        
        # Analyze categories
        self.category_patterns = self.analyze_categories()
        
        # Find optimal thresholds
        thresholds = self.find_optimal_thresholds()
        
        # Calculate metrics for each threshold
        self.results = []
        for threshold in thresholds:
            metrics = self.calculate_threshold_metrics(threshold)
            self.results.append(metrics)
        
        return AnalysisResults(self)
    
    def save_report(self, output_path: str = "threshold_analysis_report.html") -> None:
        """Generate and save HTML report."""
        if self.results is None:
            raise ValueError("No analysis results. Run analyze() first.")
            
        # Create visualizations
        fig = create_visualizations(self.df, self.results, self.config)
        
        # Clean up dataset name (remove extension)
        dataset_name = os.path.splitext(os.path.basename(output_path))[0]
        
        # Generate report
        report_html = generate_report(
            df=self.df,
            results=self.results,
            config=self.config,
            dataset_name=dataset_name,
            output_path=output_path,
            fig=fig
        )
        
        # Save report
        with open(output_path, 'w') as f:
            f.write(report_html)

@dataclass
class AnalysisResults:
    """Container for analysis results."""
    
    analyzer: ThresholdAnalyzer
    
    @property
    def thresholds(self) -> List[float]:
        """Get list of thresholds."""
        return [m.threshold for m in self.metrics]
    
    @property
    def metrics(self) -> List[ThresholdMetrics]:
        """Get list of threshold metrics."""
        return self.analyzer.results
    
    @property
    def category_patterns(self) -> Optional[pl.DataFrame]:
        """Get category analysis results."""
        return self.analyzer.category_patterns
    
    def save_report(self, output_path: str = "threshold_analysis_report.html") -> None:
        """Generate and save HTML report."""
        self.analyzer.save_report(output_path)
    
    def __str__(self) -> str:
        """Human-readable string representation."""
        lines = ["Analysis Results:"]
        for i, metrics in enumerate(self.metrics, 1):
            risk_level = ["Warning", "High Risk", "Critical"][min(i-1, 2)]
            lines.append(f"\n{risk_level} Threshold:")
            lines.append(str(metrics))
        return "\n".join(lines) 