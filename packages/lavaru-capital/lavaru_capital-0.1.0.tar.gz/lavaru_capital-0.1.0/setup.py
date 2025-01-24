from setuptools import setup, find_packages

setup(
    name="lavaru_capital",
    version="0.1.0",
    author="megavaru",
    author_email="anon@anon.anon",
    description="De la megavaru pentru veri",
    package_dir={"": "src"},  # Look for packages in the `src` directory
    packages=find_packages(where="src"),  # Automatically find packages in `src`
    install_requires=[
        "pandas_ta",
        "pandas",
        "ccxt",
        "numpy",
        "plotly",
    ],
    python_requires=">=3.13",  # Requires Python 3.13 or higher
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # Match your chosen license
        "Operating System :: OS Independent",
    ],
)


