from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="deepseek-cli",
    version="0.1.6",
    author="PierrunoYT",
    author_email="pierrebruno@hotmail.ch",
    description="A powerful CLI for interacting with DeepSeek's AI models",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/PierrunoYT/deepseek-cli",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.7",
    install_requires=[
        "openai>=1.0.0",
    ],
    entry_points={
        "console_scripts": [
            "deepseek=src.cli.deepseek_cli:main",
        ],
    },
) 