from setuptools import setup, find_packages

setup(
    name="louvain-enhanced",
    version="0.1",
    author="himangshu",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "networkx",
        "numpy",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)