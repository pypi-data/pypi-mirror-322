from setuptools import setup, find_packages

setup(
    name="db_library",
    version="0.2",
    packages=find_packages(),
    author="Alexandr Ignatiev",
    author_email="frive9007@gmail.com",
    description="A library for working with PostgreSQL 2",
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)