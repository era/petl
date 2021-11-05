from setuptools import setup

setup(name='petl',
      version='0.0.1',
      author='Elias Granja',
      author_email='me@elias.sh',
      license='AGPLv3',
      packages=['petl'],
      install_requires=[
          'TwitterAPI',
      ],
      zip_safe=False)
