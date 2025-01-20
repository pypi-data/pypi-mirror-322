from setuptools import setup, find_packages

setup(
    name="PyModelTrainer",
    version="0.0.1",
    description="Train multiple regression models and return the best one.",
    author="Nchiket",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "scikit-learn",
    ],
    python_requires=">=3.7",
)
