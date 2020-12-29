from setuptools import setup, find_packages

setup(name='deflate',
      version='1.0',
      url='https://github.com/KeiserKholod/deflate',
      description='CLI DEFLATE compressor and decompressor',
      packages=find_packages(),
      test_suite='tests',
      install_requires=['bitarray'],
      entry_points={
          'console_scripts': ['deflate=deflate.__main__']
      }
      )
