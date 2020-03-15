__license__ = open('LICENSE').read()
version = open('VERSION').read()

from setuptools import setup

long_description = open('README.md').read()

setup(
  name    = 'bulmate',
  version = version,
  author  = 'gardsted',
  author_email = 'gardsted@gmail.com',
  license = 'MIT',
  url     = 'https://github.com/gardsted/bulmate/',
  description      = 'Bulmate is a Python library for dominating CCCP with Bulma',
  long_description = long_description,
  long_description_content_type='text/markdown',
  keywords         = 'framework templating template html xhtml python html5 css bulma',

  python_requires='>=3.5.*',
  classifiers = [
    'Intended Audience :: Developers',
    'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Topic :: Text Processing :: Markup :: HTML',
  ],

  packages = ['bulmate'],
  requirements = ["cccp", "dominate"],
  include_package_data = True,
)
