#!/usr/bin/env python

import os

from pip.req import parse_requirements
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst'), 'r') as fh:
    readme = fh.read()

requirements = parse_requirements(
    os.path.join(os.path.dirname(__file__), 'requirements.txt'))
install_requires = [str(req.req) for req in requirements]

setup(name='Django-billometer',
      version=__import__('billometer').__version__,
      description='Openstack billing service.',
      long_description=readme,
      author='Ales Komarek',
      author_email='mail@newt.cz',
      url='http://newt.cz/',
      license='BSD License',
      platforms=['OS Independent'],
      packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
      include_package_data=True,
      install_requires=install_requires,
      classifiers=[
          'Development Status :: 1 - Alpha',
          'Environment :: Web Environment',
          'Framework :: Django',
          'Intended Audibillometere :: Developers',
          'License :: OSI Approved :: BSD License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
          'Topic :: Software Development',
          'Topic :: Software Development :: Libraries :: Application Frameworks',
      ],
      )
