from __future__ import print_function

from setuptools import setup, find_packages


setup(name='aiohttp_themes',
      version='0.0.2',
      description='Aiohttp Chat Example',
      long_description='',
      classifiers=[
          'Development Status :: 2 - Pre-Alpha',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.5',
      ],
      keywords='asyncio aiohttp frontend themes sass',
      url='https://github.com/storborg/aiohttp_themes',
      author='Scott Torborg',
      author_email='storborg@gmail.com',
      license='MIT',
      packages=find_packages(),
      install_requires=[
          'aiohttp',
          'mako>=1.0.4',
          'libsass',
      ],
      test_suite='nose.collector',
      tests_require=['nose'],
      include_package_data=True,
      zip_safe=False)
