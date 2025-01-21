from setuptools import setup, find_packages

setup(
    name="rexlogger",
    version="0.1.0",
    author="ReXx™",
    author_email="r3x.fr5@gmail.com",
    description="A stylish console logger with colored output",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",  
    url="https://github.com/iblamerex/Rexlogger",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "colorama>=0.4.4",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
