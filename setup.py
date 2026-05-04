from setuptools import setup, find_packages

setup(
    name="insighta",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "click",
        "requests"
    ],
    entry_points={
        "console_scripts": [
            "insighta=insighta.main:cli"
        ]
    }
)