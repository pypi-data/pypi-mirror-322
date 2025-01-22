from setuptools import setup, find_packages

setup(
    name="celery-redis-cluster",
    version="0.1.3",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "celery>=5.3.0",
        "redis>=4.5.0",
    ],
    author="Lev Neiman",
    author_email="lev.neiman@gmail.com",
    description="A Redis Cluster backend for Celery",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/lan17/celery-redis-cluster",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
)
