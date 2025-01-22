# LeadIndicator

A Python package for analyzing leading indicators and finding optimal thresholds.

## Features

- Analyze time series data to identify leading indicators
- Find optimal thresholds using multiple metrics
- Generate comprehensive analysis reports
- Support for categorical analysis
- Beautiful visualizations
- Polars-based for high performance

## Installation

```bash
pip install leadindicator
```

## Quick Start

```python
import polars as pl
from leadindicator import ThresholdAnalyzer

# Load your data
df = pl.read_excel("your_data.xlsx")

# Create analyzer
analyzer = ThresholdAnalyzer(
    score_column="score",
    target_column="event",
    category_column="category"  # Optional
)

# Run analysis
results = analyzer.analyze(df)

# Generate report
analyzer.save_report("analysis_report.html")
```

## Example: Fruit Spoilage Analysis

The package includes an example that demonstrates how to use LeadIndicator to analyze fruit spoilage data:

```python
from leadindicator import ThresholdAnalyzer
import polars as pl

# Load example data
df = pl.read_excel("Test Data.xlsx")

# Create analyzer
analyzer = ThresholdAnalyzer(
    score_column="Ethylene",
    target_column="Spoiled",
    category_column="Fruit Type"
)

# Run analysis
results = analyzer.analyze(df)

# Save report
analyzer.save_report("fruit_spoilage_analysis.html")

# Access results programmatically
best_threshold = results[0]
print(f"Best threshold: {best_threshold.threshold}")
print(f"Balanced accuracy: {best_threshold.balanced_accuracy:.2%}")
print(f"Capture rate: {best_threshold.capture_rate:.1f}%")
print(f"Event probability: {best_threshold.event_probability:.1f}%")
```

## Documentation

For detailed documentation, visit [docs/](docs/).

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 