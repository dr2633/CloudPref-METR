from setuptools import setup, find_packages

setup(
    name="cloudpref-metr",
    version="0.1.0",
    author="Derek Rosenzweig",
    author_email="derek.rosenzweig1@gmail.com",
    description="A framework for evaluating cloud provider preferences in LLMs",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/dr2633/cloudpref-metr",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=[
        "numpy",
        "pandas",
        "matplotlib",
        "seaborn",
        "jupyter",
    ],
    extras_require={
        "dev": [
            "pytest",
            "flake8",
            "black",
            "mypy",
        ],
    },
)