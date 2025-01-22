from setuptools import setup, find_packages

setup(
    name="pylwr",
    version="1.0.21",
    author="linwr",
    author_email="953297255@qq.com",
    description="各种包使用的二次封装",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://gitee.com/linwanrui/pylwr",
    license="GPL-3.0-only",
    license_files=['LICENSE'],  # 使用正确的字段
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.10",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
)
