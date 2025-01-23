from setuptools import setup, find_packages

setup(
    name="otc_backtest",
    version="1.0.2",
    author="gjnina",
    author_email="gjnina726@163.com",
    description="A package for generating contracts",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/gjnina/otc_backtest",
    packages=find_packages(),  # 自动发现所有包和子包
    include_package_data=True,  # 包含非代码文件
    package_data={
        "otc_backtest.calendar": ["China/*.txt"],  # 包含 calendar/China 中的 .txt 文件
        "otc_backtest.data": ["*.csv"]  # 包含 data 文件夹中的 CSV 文件
    },
    install_requires=[
        "pandas",
        "fleet"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)