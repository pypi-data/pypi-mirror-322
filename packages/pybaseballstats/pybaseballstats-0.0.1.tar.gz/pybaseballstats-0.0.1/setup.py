from setuptools import find_packages, setup

setup(
    name="pybaseballstats",
    version="0.0.1",
    packages=find_packages(include=["pybaseballstats", "pybaseballstats.*"]),
    # other setup arguments
)
