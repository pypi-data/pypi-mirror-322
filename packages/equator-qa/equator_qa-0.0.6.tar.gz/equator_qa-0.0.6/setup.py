# setup.py
from setuptools import setup, find_packages

setup(
    name="equator_qa",
    version="0.0.5",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.18.0",
        "requests>=2.25.0",
        "jupyter",
        # Add other runtime dependencies here
    ],
    extras_require={
        "dev": [
            "pytest",
            "pytest-mock",
            "flake8",
            "twine"
            "bump2version",  # Add this line

            # Add other development dependencies here
        ],
    },
    entry_points={
        "console_scripts": [
            "equator = equator_qa.main:main",
        ],
    },
    package_data={
        "equator_qa": ["data/*", "assets/*"],
    },
    # Include other necessary metadata
)
