from setuptools import setup, find_packages

setup(
    name="rawana",
    version="0.1.2",
    author="Ishan Oshada",
    author_email="ishan.kodithuwakku.offical@gmail.com",
    description="A package about Rawana's super powers and stories",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ishanoshada/rawana",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
