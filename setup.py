import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='csmtiser',
    version='0.0.1',
    packages=['csmtiser'],
    include_package_data=True,
    license='MIT License',
    description='A tool for text normalisation via character-level machine translation',
    long_description=README,
    url='https://github.com/clarinsi/csmtiser',
    author='Matic Perovsek',
    author_email='matic.perovsek@ijs.si',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Software Development :: Libraries'
    ],
    install_requires=[
    ]
)
