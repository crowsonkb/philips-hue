from setuptools import setup

setup(name='philips-hue',
      version='0.1',
      description='A CLI tool to interface with Philips Hue lights.',
      url='http://github.com/crowsonkb/philips-hue',
      author='Katherine Crowson',
      author_email='crowsonkb@gmail.com',
      license='MIT',
      packages=['philips_hue'],
      install_requires=['requests >= 2.18.4',
                        'prompt-toolkit >= 1.0.15',
                        'Pygments >= 2.2.0',
                        'qhue >= 1.0.9'],
      entry_points={
          'console_scripts': ['philipshue=philips_hue.cli:main'],
      })
