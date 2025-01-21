from setuptools import setup, find_packages

setup(
    name="ollehudga",
    version="0.2",
    packages=find_packages(),
    install_requires=[
        # add your dependencies
    ],
    entry_points={
        "console_scripts":[
            "ollehudga = ollehudga_hello:hello",
        ],
    },
)