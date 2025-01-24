from setuptools import setup, find_packages

setup(
    name="hyperlpr2",  # 包名
    version="2.0.0",  # 版本号，确保与上次不同
    author="liu",
    author_email="1003662721@qq.com",
    description="hyperlpr添加opencv>=4.11与numpy>1.22.0支持",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://gitee.com/zeusees/HyperLPR",  # 项目主页
    packages=find_packages(),
    include_package_data=True,  # 启用包含非代码文件
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_data={
        # 指定需要包含的文件
        "hyperlpr2": [
            "models/**/*",
        ]
    },
    python_requires='>=3.6',
    install_requires=[
        # 依赖项
        "opencv-python"
    ],
)
