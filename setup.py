from setuptools import setup, find_packages

setup(
    name="ai_job_matcher",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "PyPDF2==3.0.1",
        "requests==2.26.0",
        "beautifulsoup4==4.10.0",
        "sentence-transformers==2.2.2",
        "scikit-learn==1.0.2",
        "numpy==1.21.5",
    ],
    entry_points={
        "console_scripts": [
            "ai_job_matcher=main:main",
        ],
    },
)