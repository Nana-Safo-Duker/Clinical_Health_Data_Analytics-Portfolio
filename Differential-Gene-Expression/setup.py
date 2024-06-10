"""
Setup script for Differential Gene Expression Dashboard
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of README
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

# Read requirements
requirements = (this_directory / "requirements.txt").read_text(encoding='utf-8').splitlines()
requirements = [req.strip() for req in requirements if req.strip() and not req.startswith('#')]

setup(
    name="differential-gene-expression-dashboard",
    version="2.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Interactive web dashboard for differential gene expression analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/Differential-Gene-Expression",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        'dev': [
            'pytest>=7.0.0',
            'pytest-cov>=4.0.0',
            'black>=23.0.0',
            'flake8>=6.0.0',
            'mypy>=1.0.0',
        ],
    },
    entry_points={
        'console_scripts': [
            'degdash=scripts.quick_start:main',
        ],
    },
    include_package_data=True,
    package_data={
        '': ['*.md', '*.txt', '*.csv'],
    },
    keywords=[
        'bioinformatics',
        'genomics',
        'differential-expression',
        'rna-seq',
        'visualization',
        'streamlit',
        'data-analysis',
    ],
    project_urls={
        'Bug Reports': 'https://github.com/yourusername/Differential-Gene-Expression/issues',
        'Documentation': 'https://github.com/yourusername/Differential-Gene-Expression/tree/main/docs',
        'Source': 'https://github.com/yourusername/Differential-Gene-Expression',
    },
)


