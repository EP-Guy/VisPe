from setuptools import setup

setup(name='vispe',
	  version='0.1',
	  description='Plot a satellite pass through the sky',
	  author='Forrest Gasdia',
	  url='https://github.com/EP-Guy/VisPe',
	  packages=['vispe'],
	  install_requires=[
	  	'numpy',
	  	'astropy',
	  	'skyfield',
	  	'pandas',
	  ],
	  include_package_data=True)