from setuptools import setup, find_packages

setup(name="hhsqllib",
	  version="0.46",
	  packages=find_packages(),
	  install_requires=[
'SQLAlchemy==2.0.30',
	  ],
	  author="hh",
	  author_email="hehuang0717@outlook.com",
	  description="sqllib",
	  long_description=open('README.md').read(),
	  long_description_content_type="text/markdown",
	  url="https://your.project.url",
	  classifiers=["Programming Language :: Python :: 3", "License :: OSI Approved :: MIT License",
				   "Operating System :: OS Independent", ],
	  python_requires='>=3.9', )
