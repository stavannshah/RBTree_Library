from setuptools import setup, find_packages

setup(
	name='assignment1',
	version='1.0',
	author='Harshit Lohaan',
	author_email='h.lohaan@ufl.edu',
	packages=find_packages(exclude=('tests', 'docs', 'resources')),
	setup_requires=['pytest-runner'],
	tests_require=['pytest']	
)