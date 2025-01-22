"""
Visualization functions for threshold analysis.
"""

import matplotlib.pyplot as plt
import seaborn as sns
from typing import List
import polars as pl
from .metrics import ThresholdMetrics

def create_visualizations(df: pl.DataFrame, results: List[ThresholdMetrics], config: 'AnalyzerConfig'):
    """Create comprehensive analysis visualizations."""
    # Create figure with subplots
    fig = plt.figure(figsize=(15, 20))
    gs = plt.GridSpec(4, 2, figure=fig)
    
    # 1. Score Distribution with Thresholds
    ax1 = fig.add_subplot(gs[0, 0])
    hist_data = df.to_pandas()[config.score_column]
    sns.histplot(data=hist_data, ax=ax1)
    ax1.set_title(f"{config.score_column} Distribution")
    ax1.set_xlabel(config.score_column)
    
    # Add threshold lines
    colors = ['r', 'y', 'g']
    for i, result in enumerate(results[:3]):
        ax1.axvline(x=result.threshold, color=colors[i], 
                   linestyle='--', alpha=0.7,
                   label=f'Threshold {result.threshold:.2f}')
    ax1.legend()
    
    # 2. Event Probability vs Score (scatter plot)
    ax2 = fig.add_subplot(gs[0, 1])
    # Calculate probabilities for different score ranges
    score_ranges = []
    probs = []
    for threshold in sorted(df[config.score_column].unique()):
        subset = df.filter(pl.col(config.score_column) >= threshold)
        if len(subset) > 0:
            event_prob = len(subset.filter(pl.col(config.target_column) > 0)) / len(subset)
            score_ranges.append(threshold)
            probs.append(event_prob)
    
    ax2.scatter(score_ranges, probs, alpha=0.6)
    ax2.set_title("Event Probability vs Score")
    ax2.set_xlabel(config.score_column)
    ax2.set_ylabel("Event Probability")
    
    # Add threshold lines
    for i, result in enumerate(results[:3]):
        ax2.axvline(x=result.threshold, color=colors[i], 
                   linestyle='--', alpha=0.7,
                   label=f'Threshold {result.threshold:.2f}')
    ax2.legend()
    
    # 3. Score Distribution by Category
    if config.category_column:
        ax3 = fig.add_subplot(gs[1, 0])
        sns.boxplot(data=df.to_pandas(), 
                   x=config.category_column,
                   y=config.score_column,
                   ax=ax3)
        ax3.set_title(f"Score Distribution by {config.category_column}")
        plt.setp(ax3.xaxis.get_majorticklabels(), rotation=45)
        
        # Add threshold lines
        for i, result in enumerate(results[:3]):
            ax3.axhline(y=result.threshold, color=colors[i],
                       linestyle='--', alpha=0.7)
    
    # 4. Event Count Distribution
    ax4 = fig.add_subplot(gs[1, 1])
    sns.histplot(data=df.to_pandas(), x=config.target_column, ax=ax4)
    ax4.set_title("Event Count Distribution")
    
    # 5. Score vs Event Count (Box Plot)
    ax5 = fig.add_subplot(gs[2, 0])
    event_counts = df[config.target_column].unique()
    box_data = []
    labels = []
    for count in sorted(event_counts):
        scores = df.filter(pl.col(config.target_column) == count)[config.score_column]
        if len(scores) > 0:
            box_data.append(scores.to_list())
            labels.append(str(count))
    
    ax5.boxplot(box_data, labels=labels)
    ax5.set_title("Score Distribution by Event Count")
    ax5.set_xlabel("Event Count")
    ax5.set_ylabel(config.score_column)
    
    # 6. Threshold Performance Metrics
    ax6 = fig.add_subplot(gs[2, 1])
    metrics_data = pl.DataFrame([{
        "threshold": r.threshold,
        "capture_rate": r.capture_rate,
        "event_probability": r.event_probability
    } for r in results])
    
    x = range(len(results))
    width = 0.35
    ax6.bar([i - width/2 for i in x], 
            metrics_data["capture_rate"].to_list(),
            width, label="Capture Rate %")
    ax6.bar([i + width/2 for i in x], 
            metrics_data["event_probability"].to_list(),
            width, label="Event Probability %")
    
    ax6.set_xticks(x)
    ax6.set_xticklabels([f"{t:.2f}" for t in metrics_data["threshold"].to_list()])
    ax6.set_title("Threshold Performance Metrics")
    ax6.legend()
    
    # 7. Time Series if date column exists
    date_cols = [col for col in df.columns if "date" in col.lower()]
    if date_cols:
        ax7 = fig.add_subplot(gs[3, :])
        date_col = date_cols[0]
        ts_data = df.sort(date_col)
        
        # Plot score over time
        ax7.plot(ts_data[date_col].to_list(), 
                ts_data[config.score_column].to_list(),
                label="Score", alpha=0.6)
        
        # Highlight events
        events = ts_data.filter(pl.col(config.target_column) > 0)
        if len(events) > 0:
            ax7.scatter(events[date_col].to_list(),
                       events[config.score_column].to_list(),
                       color='red', label="Events", alpha=0.6)
        
        ax7.set_title("Score and Events Over Time")
        ax7.legend()
        plt.setp(ax7.xaxis.get_majorticklabels(), rotation=45)
    
    plt.tight_layout()
    return fig

def plot_threshold_analysis(
    df: pl.DataFrame,
    score_column: str,
    target_column: str,
    thresholds: List[float],
    category_column: str = None
) -> plt.Figure:
    """
    Create a quick threshold analysis plot.
    
    This is a simplified version for quick exploration.
    For full analysis, use ThresholdAnalyzer.
    """
    from .analyzer import AnalyzerConfig, ThresholdAnalyzer
    
    # Create temporary analyzer
    analyzer = ThresholdAnalyzer(
        score_column=score_column,
        target_column=target_column,
        category_column=category_column
    )
    analyzer.df = df
    
    # Calculate metrics
    results = [analyzer.calculate_threshold_metrics(t) for t in thresholds]
    
    # Create visualization
    return create_visualizations(df, results, analyzer.config) 