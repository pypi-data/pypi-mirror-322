from setuptools import find_packages, setup

with open("app/README.md", "r") as f:
    long_description = f.read()

setup(
    name="multilingual_python",
    version="0.0.10",
    description="A package that allows you to write basic python in multiple languages",
    package_dir={"": "app"},
    packages=find_packages(where="app"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aadityayadav/translate_lib",
    author="Aaditya Yadav/ Aditya Swarup",
    author_email="aadityayadav2003@gmail.com, adityaswrup78@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.5",
        "Operating System :: OS Independent",
    ],
    install_requires=[],
    extras_require={
        "dev": ["pytest>=7.0", "twine>=4.0.2", "python-dotenv>=1.0.0", "wheel>=0.37.0"],
    },
    python_requires=">=3.5",
)