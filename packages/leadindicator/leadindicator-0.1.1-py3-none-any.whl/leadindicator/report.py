"""
Report generation functionality for threshold analysis.
"""

import os
import io
import base64
from datetime import datetime
from typing import List, Dict, Any, Optional
import matplotlib.pyplot as plt
from jinja2 import Environment, PackageLoader, select_autoescape
import polars as pl

from .metrics import ThresholdMetrics
from .visualization import create_visualizations

def generate_report(
    df: pl.DataFrame,
    results: List[ThresholdMetrics],
    config: 'AnalyzerConfig',
    dataset_name: str = "Dataset",
    output_path: Optional[str] = None,
    fig: Optional[plt.Figure] = None
) -> str:
    """
    Generate an HTML report from the analysis results.
    
    Args:
        df: The analyzed DataFrame
        results: List of ThresholdMetrics objects
        config: The analyzer configuration
        dataset_name: Name of the dataset for display
        output_path: Optional path to save the report
        fig: Optional pre-generated figure
        
    Returns:
        str: The HTML report content
    """
    # Create Jinja environment
    env = Environment(
        loader=PackageLoader('leadindicator', 'templates'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('report.html')
    
    # Generate plot and convert to base64
    if fig is None:
        fig = create_visualizations(df, results, config)
    
    img_data = io.BytesIO()
    fig.savefig(img_data, format='png', bbox_inches='tight')
    plt.close(fig)
    img_data.seek(0)
    plot_data = base64.b64encode(img_data.getvalue()).decode()
    
    # Calculate category metrics if category column exists
    category_metrics = None
    if config.category_column:
        category_metrics = []
        for category in sorted(df[config.category_column].unique()):
            subset = df.filter(pl.col(config.category_column) == category)
            event_count = len(subset.filter(pl.col(config.target_column) > 0))
            event_rate = event_count / len(subset) if len(subset) > 0 else 0
            category_metrics.append({
                "category": category,
                "record_count": len(subset),
                "event_count": event_count,
                "event_rate": event_rate,
                "avg_score": subset[config.score_column].mean(),
                "std_score": subset[config.score_column].std()
            })
        # Sort by event rate in descending order
        category_metrics.sort(key=lambda x: x["event_rate"], reverse=True)
    
    # Prepare template context
    context = {
        "dataset_name": dataset_name,
        "score_column": config.score_column,
        "target_column": config.target_column,
        "category_column": config.category_column,
        "total_records": len(df),
        "analysis_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "top_results": results[:3],  # Show top 3 thresholds
        "category_metrics": category_metrics,
        "plot_data": plot_data,
        "version": "0.1.0",  # TODO: Get from package metadata
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # Render template
    html_content = template.render(**context)
    
    # Save to file if output path provided
    if output_path:
        output_dir = os.path.dirname(output_path)
        if output_dir:  # Only create directory if path has a directory component
            os.makedirs(output_dir, exist_ok=True)
        with open(output_path, 'w') as f:
            f.write(html_content)
    
    return html_content 