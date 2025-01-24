from setuptools import setup, find_packages

setup(
    name="alidanish_package_two",
    version="0.1.0",
    author="Danish Ali",
    author_email="danish.ali@protonshub.in",
    description="A simple example package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/danish-protonshub/alidanish_package_two",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
