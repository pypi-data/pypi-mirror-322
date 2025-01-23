from setuptools import setup, find_packages

setup(
    name="esseppi",  # Name of the package
    version="0.4.2",  # Package version
    description="A shared utilities library for data processing, analysis, and interpretation.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Esseppi Zeta",  # Author name
    author_email="lozingaro@duck.com",  # Author email
    license="Creative Common",  # License type
    packages=find_packages(),  # Automatically find sub-packages
    install_requires=[
        "numpy",
        "pandas",
        "matplotlib",
        "psutil",  # Include required dependencies
        "joblib",
        "shap",
        "scikit-learn"
    ],
    python_requires=">=3.7",  # Specify Python version requirement
)
