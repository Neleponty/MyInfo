import ez_setup
ez_setup.use_setuptools()
from setuptools import setup

setup(
  name='ispras',
  version='1.0.2',
  packages=['ispras'],
  install_requires=[
      'requests',
      'xmltodict'
  ],
  py_modules=['ispras'],
)
