import polars as pl
from leadindicator import ThresholdAnalyzer

df = pl.read_excel("sample_data.xlsx")
df.head()
# Create analyzer with default settings
analyzer = ThresholdAnalyzer(
    score_column="Leading Indicator Score (High is Bad)",  # Leading indicator
    target_column="Fruit Spoil Count",  # Target event
    category_column="Fruit"  # Category for segmentation
)

results = analyzer.analyze(df)
print(results)
#analyzer.save_report("fruit_spoilage_analysis.html")


analyzer2 = ThresholdAnalyzer(
    score_column="Leading Indicator Score (High is Bad)",  # Leading indicator
    target_column="Fruit Spoil Count",  # Target event
    category_column="Fruit",  # Category for segmentation
    percentile_thresholds=[.2,.5,.9]
)

results2 = analyzer2.analyze(df)
print(results2)
analyzer2.save_report("fruit_spoilage_analysis.html")