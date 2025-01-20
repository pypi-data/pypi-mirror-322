from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="salesforce-spark-connector",
    version="0.1.0",
    author="T Mohan Reddy",
    author_email="timmapuramreddy@gmail.com",
    description="A scalable Python connector for Salesforce with multiple data processing engines",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/timmapuramreddy/salesforce-spark-connector",
    packages=find_packages(exclude=["tests*"]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Database",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.25.0",
        "simple-salesforce>=1.12.4",
        "requests-oauthlib>=1.3.1",
        "python-dotenv>=0.19.0",
        "pandas>=1.3.0",
        "pyarrow>=14.0.1"
    ],
    extras_require={
        'spark': ["pyspark>=3.0.0"],
        'duckdb': ["duckdb>=0.9.0"],
        'dev': [
            "pytest>=6.0.0",
            "pytest-cov>=2.0.0",
            "flake8>=3.9.0",
            "black>=21.0",
            "mypy>=0.900",
            "twine>=3.4.0",
            "build>=0.7.0"
        ],
    }
) 