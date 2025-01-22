"""
Tests for the ThresholdAnalyzer class.
"""

import pytest
import polars as pl
import numpy as np
from leadindicator import ThresholdAnalyzer

@pytest.fixture
def sample_data():
    """Create sample data for testing."""
    np.random.seed(42)
    n_samples = 100
    
    # Generate synthetic data
    scores = np.random.normal(loc=50, scale=15, size=n_samples)
    events = np.where(scores > 65, 1, 0)
    categories = np.random.choice(['A', 'B', 'C'], size=n_samples)
    
    return pl.DataFrame({
        'score': scores,
        'event': events,
        'category': categories
    })

@pytest.fixture
def analyzer(sample_data):
    """Create analyzer instance with sample data."""
    analyzer = ThresholdAnalyzer(
        score_column='score',
        target_column='event',
        category_column='category'
    )
    analyzer.df = sample_data
    return analyzer

def test_threshold_spacing():
    """Test that thresholds are properly spaced."""
    # Create data with clear threshold points
    df = pl.DataFrame({
        'score': [1, 2, 3, 4, 5] * 20,
        'event': [0, 0, 1, 1, 1] * 20
    })
    
    analyzer = ThresholdAnalyzer(
        score_column='score',
        target_column='event',
        min_threshold_spacing=0.2
    )
    
    results = analyzer.analyze(df)
    thresholds = [m.threshold for m in results.metrics]
    
    # Check spacing between thresholds
    for i in range(1, len(thresholds)):
        spacing = thresholds[i] - thresholds[i-1]
        assert spacing >= (max(df['score']) - min(df['score'])) * 0.2

def test_metrics_calculation(analyzer):
    """Test basic metrics calculation."""
    metrics = analyzer.calculate_threshold_metrics(60)
    
    assert 0 <= metrics.sensitivity <= 100
    assert 0 <= metrics.specificity <= 100
    assert 0 <= metrics.precision <= 100
    assert 0 <= metrics.f1_score <= 100
    assert 0 <= metrics.event_probability <= 100
    assert metrics.n_observations > 0

def test_category_analysis(analyzer):
    """Test category-level analysis."""
    patterns = analyzer.analyze_categories()
    
    assert len(patterns) == 3  # A, B, C categories
    assert all(col in patterns.columns for col in [
        'avg_event_rate', 'avg_score', 'n_observations',
        'n_events', 'total_events', 'max_events'
    ])

def test_invalid_config():
    """Test configuration validation."""
    with pytest.raises(ValueError):
        ThresholdAnalyzer(
            score_column='score',
            target_column='event',
            min_capture_rate=150  # Invalid value
        )
    
    with pytest.raises(ValueError):
        ThresholdAnalyzer(
            score_column='score',
            target_column='event',
            min_threshold_spacing=1.5  # Invalid value
        ) 