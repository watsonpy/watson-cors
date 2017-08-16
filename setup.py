# -*- coding: utf-8 -*-
import os
from setuptools import setup, Command
import watson.cors


class BaseCommand(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass


class PyTest(BaseCommand):
    """Runs all the unit tests.
    """
    def run(self):
        os.system('py.test')
        clean()


class PyPiPublish(BaseCommand):
    """Publishes the code to PyPi.
    """
    def run(self):
        if (confirm('Are you sure you want to push to PyPi?')):
            os.system('python setup.py sdist bdist_wheel upload')
            clean()


def clean():
    """Cleans the source directory of all non-source files.
    """
    os.system('rm -rf .coverage')
    os.system('find . -name "__pycache__" -print0|xargs -0 rm -rf')
    os.system('find . -name "*.egg-info" -print0|xargs -0 rm -rf')
    os.system('rm -rf dist')


def confirm(prompt):
    prompt += ' (Y/N) [n]: '
    while True:
        answer = input(prompt).upper()
        if not answer:
            answer = 'N'
        return False if answer != 'Y' else True

path = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(path, 'LICENSE')) as f:
    license = f.read()

with open(os.path.join(path, 'README.rst')) as f:
    readme = f.read()

with open(os.path.join(path, 'requirements.txt')) as f:
    requirements = f.read().splitlines()


setup(
    name='watson-cors',
    version=watson.cors.__version__,
    url='http://github.com/bespohk/watson-cors',
    description='CORS support for watson-framework.',
    long_description=readme,

    author='Simon Coulton',
    author_email='simon@bespohk.com',

    license=license,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Middleware',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Server'
    ],
    platforms=['Python 3.4'],
    keywords=['watson',
              'python3',
              'web framework',
              'framework',
              'wsgi',
              'web'],

    packages=['watson', 'watson.cors'],
    include_package_data=True,

    zip_safe=False,
    install_requires=requirements,

    cmdclass={
        'test': PyTest,
        'publish': PyPiPublish
    }
)
