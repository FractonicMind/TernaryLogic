"""Setup configuration for Ternary Logic Framework."""
from setuptools import setup, find_packages

setup(
    name="ternary-logic",
    version="1.0.0",
    author="Lev Goukassian",
    author_email="leogouk@gmail.com",
    description="Ternary Logic Framework for Economic Decision-Making",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.20.0",
        "pandas>=1.3.0",
    ],
    extras_require={
        "test": [
            "pytest>=7.0.0",
            "pytest-cov>=3.0.0",
            "pytest-mock>=3.6.0",
        ],
    },
)
