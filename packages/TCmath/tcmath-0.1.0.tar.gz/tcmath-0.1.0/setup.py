from setuptools import setup, find_packages

setup(
    name="TCmath",
    version="0.1.0",
    description="A library for calculating combinations, permutations, and factorials.",
    author="Nguyen Truong Chinh",
    author_email="chinhcuber@gmail.com",
    packages=find_packages(),
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    long_description=open('README.md').read(),  # Mô tả thư viện dài từ tệp README.md
    long_description_content_type="text/markdown", 
)
