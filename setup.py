#!/usr/bin/env python

from setuptools import setup, find_packages
import zssget

setup(
    name='zssget',
    version=zssget.__version__,
    description='zangsisi downloader',
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.0",
        "Programming Language :: Python :: 3.1",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Internet",
        "Topic :: Multimedia",
        "Topic :: Multimedia :: Graphics",
        "Topic :: Utilities"
    ],
    keywords='zss-get zssget download zangsisi',
    author='Sung Ho Kim',
    author_email='likeleon@gmail.com',
    maintainer='Sung Ho Kim',
    maintainer_email='likeleon@gmail.com',
    url='https://github.com/likeleon/zss-get',
    license='GPLv3',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'zssget = zssget.zssget:main'
        ]
    },
    install_requires=[
        'beautifulsoup4'
    ],
)