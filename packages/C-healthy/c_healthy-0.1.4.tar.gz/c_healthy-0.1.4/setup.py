from setuptools import setup, find_packages

setup(
    name="C_healthy",
    version="0.1.4",
    description="A library for calculating body index include: [BMI, BMR, TDEE, WHR, LBM, BFP, NW, IBW, MA]",
    author="Nguyen Truong Chinh",
    author_email="chinhcuber@gmail.com",
    packages=find_packages(),
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    long_description=open('README.md', encoding='utf-8').read(),  # Đảm bảo đọc file bằng UTF-8 # Mô tả thư viện dài từ tệp README.md
    long_description_content_type="text/markdown", 
)
