from setuptools import setup, find_packages

import pathlib

LIB_NAME = 'mangagraph'

__version__ = '0.0.1'

setup(
    name='mangagraph',
    version=__version__,
    description='Async manga parser-converter from mangalib to telegraph pages',
    url='https://github.com/damirTAG/mangagraph',
    author='damirTAG',
    author_email='damirtagilbayev17@gmail.com',
    packages=find_packages(),
    install_requires=[
        'aiohttp',
        'sqlalchemy',
        'telegraph',
        'asyncio'
    ],
    entry_points={
        'console_scripts': [
            'mangagraph= mangagraph.cli:main'
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    keywords=[
        'mangalib',
        'mangalib-parser',
        'manga',
        'telegraph'
    ],
    python_requires='>=3.7',
    include_package_data=False
)