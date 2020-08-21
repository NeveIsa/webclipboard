
from setuptools import setup

setup(name='webclipboard',
      version='0.1.1',
      description='Share your clipboard using the web.',
      url='https://github.com/NeveIsa/webclipboard',
      author='Sampad B Mohanty',
      author_email='smpdmohanty@gmail.com',
      license='GNU GPLv3',
      packages=['webclipboard'],
      install_requires=['clipboard','notify-py','pyyaml','requests'],
      zip_safe=False,
      scripts=['bin/webclipboard'],
      )
