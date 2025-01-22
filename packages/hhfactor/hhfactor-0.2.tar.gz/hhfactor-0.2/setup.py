from setuptools import setup, find_packages

setup(name="hhfactor",
	  version="0.2",
	  packages=find_packages(),
	  install_requires=[],
	  author="hh",
	  author_email="hehuang0717@outlook.com",
	  description="factor",
	  long_description=open('README.md').read(),
	  long_description_content_type="text/markdown",
	  url="https://your.project.url",
	  classifiers=["Programming Language :: Python :: 3", "License :: OSI Approved :: MIT License",
				   "Operating System :: OS Independent", ],
	  python_requires='>=3.9', )
