from setuptools import setup, find_packages

setup(
    name="EquationPlot",
    version="0.1.1",
    description="A library to plot mathematical equations on a graph.",
    long_description=open("README.md").read(),
    long_description_content_type='text/markdown', 
    author="Diksha, Ayush Kumar Verma",
    author_email="diksha260303official@gmail.com",
    url="https://medium.com/@diksha260303official/equationplot-a-python-library-for-effortless-graphing-of-mathematical-equations-c6270d2a15d1",
    packages=find_packages(),
    install_requires=[
        "matplotlib",
        "sympy",
        "numpy"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.5",
)
