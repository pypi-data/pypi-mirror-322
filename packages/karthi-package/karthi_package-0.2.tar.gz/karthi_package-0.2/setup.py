from setuptools import setup, find_packages

setup(
    name="karthi_package",  
    version="0.2",
    description="A package for numerical operations using NumPy",
    author="karthi",
    author_email="karthi@gmail.com",
    packages=find_packages(), 
    install_requires=[
        "numpy>=1.21.0",  
    ],
)
