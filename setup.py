from setuptools import setup, find_packages
import sys

sys.path.append('./test')

setup(
	name = 'testDeimFunctions',
	version = '0.1',
	desription = 'Test codes for deimscripts',
	packages = find_packages(),
	test_suite = 'testDeimFunctions.suite'
)
