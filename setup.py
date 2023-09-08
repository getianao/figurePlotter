from setuptools import setup

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="figurePlotter",
    version="0.0.1",
    author="TianaoGe",
    author_email="getianao@gmail.com",
    description="Making publication-quality figures in Python.",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/getianao/figurePlotter",
    packages=['figurePlotter'],
    install_requires=requirements,
    python_requires='>=3.8',
)