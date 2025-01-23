# setup.py
from setuptools import setup, find_packages

setup(
    name="deeptechv_ai",
    version="0.1.0",
    author="Techvantage",
    description="Techvantage AI Developer Toolkit for Deepseek",
    packages=find_packages(),
    install_requires=["openai", "requests"],
    entry_points={
        "console_scripts": [
            "deeptechv_ai=deeptechv_ai.__main__:main"
        ]
    },
)