from setuptools import setup, find_packages

setup(
    name="pytest_ai",
    version="0.1.0",
    description="A Python package to generate regular, edge-case, and security HTTP tests.",
    author="jobran628",
    author_email="jobran628@gmail.com",
    license="Apache License 2.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "pydantic",
        "python-dotenv",
        "langchain",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
