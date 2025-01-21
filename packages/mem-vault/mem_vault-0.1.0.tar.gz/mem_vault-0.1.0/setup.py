from setuptools import setup, find_packages

setup(
    name="mem_vault",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.19.0",
        "openai>=1.0.0",
        "sqlalchemy>=1.4.0",
        "psycopg2-binary>=2.9.0",
        "pgvector>=0.2.0",
        "regex>=2023.0.0",  # For better text processing
    ],
    extras_require={
        'django': ['django>=3.2'],
    },
    author="Jitin Pillai",
    author_email="me@jitinpillai.com",
    description="A library for storing and retrieving embeddings with PGVector (with Chunking)",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Instadeploy/mem-vault",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
) 