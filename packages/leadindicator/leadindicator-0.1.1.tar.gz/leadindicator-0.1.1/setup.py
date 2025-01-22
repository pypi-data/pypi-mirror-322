from setuptools import setup, find_packages

setup(
    name="leadindicator",
    version="0.1.0",
    description="A package for analyzing leading indicators and finding optimal thresholds",
    author="Allen Fruit",
    author_email="allen@example.com",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "polars>=0.20.0",
        "matplotlib>=3.5.0",
        "seaborn>=0.12.0",
        "jinja2>=3.0.0",
    ],
    package_data={
        "leadindicator": ["templates/*.html"],
    },
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Information Analysis",
    ],
) 