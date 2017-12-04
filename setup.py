from setuptools import setup

setup(name='twitchchatanalyzer',
      version='0.1',
      description='Tools for analyzing twitch chat.',
      url='',
      author='Augusto Cesar',
      author_email='augusto.acfs@gmail.com',
      license='MIT',
      packages=['twitchchatanalyzer'],
      install_requires=[
          'pyyaml',
          'peewee'
      ],
      zip_safe=False)
