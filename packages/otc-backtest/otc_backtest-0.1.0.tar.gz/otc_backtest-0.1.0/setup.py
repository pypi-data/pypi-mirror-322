from setuptools import setup, find_packages

setup(
    name="otc_backtest",
    version="0.1.0",
    author="gjnina",
    author_email="gjnina726@163.com",
    description="",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/gjnina/backtest",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "datetime",
        "pandas",
        "fleet"
        # ...
    ],
)