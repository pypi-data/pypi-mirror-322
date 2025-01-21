from setuptools import setup, find_packages

with open("README.md", "r") as f:
    description = f.read()

setup(
    name="ollehudga",
    version="0.4.4",
    packages=find_packages(),
    install_requires=[
        # add your dependencies
    ],
    entry_points={
        "console_scripts":[
            "ollehudga = ollehudga_p1:p1",
        ],
    },

    long_description=description,
    long_description_content_type="text/markdown"
)