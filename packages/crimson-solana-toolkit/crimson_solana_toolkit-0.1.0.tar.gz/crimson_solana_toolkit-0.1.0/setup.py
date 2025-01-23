from setuptools import setup, find_packages

setup(
    name="crimson-solana-toolkit",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "solana",
        "anchorpy",
        "base58",
        "construct",
        "pytest",
        "pytest-asyncio",
        "crimson-agent",  # Dependency on crimson-agent package
        "pandas",
        "numpy",
        "networkx",
        "plotly",
        "scipy",
        "matplotlib",
        "seaborn"
    ],
    author="Crimson Labs",
    author_email="crimsonlabsai@gmail.com",
    description="A comprehensive Solana blockchain toolkit for the Crimson Labs ecosystem.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/crimson-labs/crimson-solana-toolkit",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Distributed Computing",
        "Topic :: Office/Business :: Financial",
        "Topic :: Security :: Cryptography",
    ],
    python_requires=">=3.8",
    extras_require={
        'dev': [
            'pytest',
            'pytest-asyncio',
            'pytest-cov',
            'black',
            'isort',
            'mypy',
            'flake8',
            'sphinx',
            'sphinx-rtd-theme'
        ],
        'docs': [
            'sphinx',
            'sphinx-rtd-theme',
            'sphinx-autodoc-typehints'
        ]
    },
    entry_points={
        'console_scripts': [
            'crimson-solana=crimson_solana_toolkit.cli:main',
        ],
    },
    project_urls={
        'Source': 'https://github.com/crimson-labs/crimson-solana-toolkit',
        'Tracker': 'https://github.com/crimson-labs/crimson-solana-toolkit/issues',
    }
)
