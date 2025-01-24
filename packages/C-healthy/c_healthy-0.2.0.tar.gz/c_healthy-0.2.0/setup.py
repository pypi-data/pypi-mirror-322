import os
from setuptools import setup, find_packages

# Đọc nội dung README.md
long_description = ""
if os.path.exists("README.md"):
    with open("README.md", encoding="utf-8") as f:
        long_description = f.read()

setup(
    name="C_healthy",
    version="0.2.0",
    description="A library for calculating body index include: [BMI, BMR, TDEE, WHR, LBM, BFP, NW, IBW, MA]",
    author="Nguyen Truong Chinh",
    author_email="chinhcuber@gmail.com",
    packages=find_packages(),
    python_requires=">=3.6",
    install_requires=[
        "sys"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords=['BMI', 'BMR', 'TDEE', 'WHR', 'LBM', 'BFP', 'NW', 'IBW', 'MA', 'HDSD'],
    long_description=long_description,
    long_description_content_type="text/markdown",
)
