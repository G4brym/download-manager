from setuptools import find_packages, setup

setup(
    name="common",
    version="0.0.0",
    packages=find_packages(),
    install_requires=[
        "injector",
        "downloads",
        "downloads_infrastructure",
    ],
)
