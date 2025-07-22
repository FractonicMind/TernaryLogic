"""
Goukassian Framework - Ternary Logic for Intelligent Decision-Making
Created by Lev Goukassian (ORCID: 0009-0006-5966-1243)
Contact: leogouk@gmail.com
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="goukassian-framework",
    version="1.0.0",
    author="Lev Goukassian",
    author_email="leogouk@gmail.com",
    description="Ternary Logic for Intelligent Decision-Making Under Uncertainty",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/FractonicMind/TernaryLogic",
    project_urls={
        "Bug Tracker": "https://github.com/FractonicMind/TernaryLogic/issues",
        "Documentation": "https://github.com/FractonicMind/TernaryLogic#readme",
        "Manifesto": "https://medium.com/@leogouk/the-third-option-why-economy-and-civilization-must-break-free-from-binary-0d69d2be14c6",
        "Creator ORCID": "https://orcid.org/0009-0006-5966-1243"
    },
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Financial and Insurance Industry",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Office/Business :: Financial",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8",
            "mypy>=0.800",
            "pre-commit>=2.0",
        ],
        "financial": [
            "yfinance>=0.1.70",
            "pandas-datareader>=0.10.0",
            "quantlib>=1.25",
        ],
        "visualization": [
            "matplotlib>=3.5.0",
            "plotly>=5.0.0",
            "seaborn>=0.11.0",
        ],
        "ml": [
            "scikit-learn>=1.0.0",
            "tensorflow>=2.8.0",
            "torch>=1.11.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "goukassian=goukassian.cli:main",
        ],
    },
    keywords=[
        "ternary-logic",
        "decision-making", 
        "uncertainty",
        "finance",
        "economics",
        "artificial-intelligence",
        "risk-management",
        "algorithmic-trading",
        "supply-chain",
        "goukassian-framework"
    ],
    license="MIT",
    zip_safe=False,
)
