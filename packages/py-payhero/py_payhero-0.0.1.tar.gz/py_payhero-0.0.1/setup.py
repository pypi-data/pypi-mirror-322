from setuptools import setup, find_packages

setup(
    name="py-payhero",
    version="0.0.1",
    description="A Python SDK for interacting with the PayHero API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Njeru Mtwaiti",
    author_email="newerbandit@proton.me",
    url="https://github.com/njeru-codes/PayHero-API-SDK-",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "requests"
    ],
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)