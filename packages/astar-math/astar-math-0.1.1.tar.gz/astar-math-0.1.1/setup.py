#!/usr/bin/env python

__author__ = 'A.Star'

from setuptools import find_packages
import astar_math
from astartool.setuptool import load_install_requires, setup
from astar_devopstool.common import Language, Plantform, License

setup(
    name="astar-math",
    version=astar_math.__version__,
    description=(
        'Python math'
    ),
    long_description=open('readme.rst', encoding='utf-8').read(),
    author='A.Star',
    author_email='astar@snowland.ltd',
    maintainer='A.Star',
    maintainer_email='astar@snowland.ltd',
    license='Apache v2.0 License',
    packages=find_packages(),
    platforms=[Plantform.ALL.value],
    url='https://gitee.com/hoops/astar-mathtool',
    classifiers=[
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        License.APACHE.value,
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Topic :: Software Development :: Libraries'
    ],
    install_requires=load_install_requires(),

)
