from setuptools import setup, find_packages

# prepare the instruction
description = "";
with open("README.md", "r") as readme:
    description = readme.read();
setup(
      name="whatshow_toolbox",
      version="1.0.10",
      packages=find_packages(),
      install_requires=['numpy>=1.20.1'],
      long_description = description,
      long_description_content_type = "text/markdown"
);