from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="textract-form-parser",
    version="0.1.6",
    author="Yogeshvar Senthilkumar",
    author_email="yogeshvar@icloud.com",
    description="A Python library for parsing AWS Textract form output",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yogeshvar/text-extractor",
    packages=find_packages(include=["textract_parser", "textract_parser.*"]),
    python_requires=">=3.8",
    install_requires=[
        "boto3>=1.26.0",
        "pandas>=1.3.0",
        "numpy>=1.19.0",
        "requests>=2.25.0",
        "packaging>=20.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "isort>=5.0.0",
            "flake8>=4.0.0",
            "pre-commit>=3.5.0",
            "commitizen>=3.13.0",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    entry_points={
        "console_scripts": [
            "textract-parser=textract_parser.__main__:main",
        ],
    },
)
