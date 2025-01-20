import setuptools

with open("DataVerification.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="data_verification",  # 包名
    version="0.0.2.1",  # 包版本号
    author="39",  # 作者名
    author_email="DY39project@outlook.com",  # 联系方式
    description="数据检验的工具",  # 包的简述
    long_description=long_description,  # 包的详细介绍
    long_description_content_type="text/markdown",
    url="https://github.com/yanshi121/DataVerification",  # 项目地址
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires='>=3.5',  # 对python的最低版本要求
    install_requires=["geopandas", "shapely"]  # 项目依赖的其他库
)
