from setuptools import find_packages, setup

setup(
    name="downloads_infrastructure",
    version="0.0.0",
    packages=find_packages(),
    install_requires=["injector", "downloads"],
    extras_require={"dev": ["pytest"]},
)
