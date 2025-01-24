from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="tdatasuite",
    version="1.0.0",
    author="ZentravaFlow",
    description="A toolkit for Telegram data collection and analytics",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ZentravaFlow/tdatasuite",
    packages=find_packages(),
    install_requires=[
        "pandas==2.2.3",
        "mtprotocrypt==1.2.6.5b0",
        "kurigram==2.1.37",
    ],
    python_requires="<=3.12.8"
)