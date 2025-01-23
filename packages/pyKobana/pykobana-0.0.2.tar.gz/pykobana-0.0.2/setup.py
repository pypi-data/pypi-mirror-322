from setuptools import setup, find_packages

setup(
    name="pyKobana",
    version="0.0.2",
    author="Dola Lima",
    author_email="dolalima@gmail.com",
    description="A simple python client for Kobana API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/dolalima/pyKobana",
    packages=find_packages(),
    install_requires=[
        "requests",
    ],
    test_suite="tests",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
