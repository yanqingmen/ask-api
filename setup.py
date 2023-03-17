# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

with open('requirements.txt', encoding='utf-8') as f:
    requirements = f.read().strip().split('\n')

pkgs = find_packages(where='src')
print(pkgs)

setup(
    name='ask-api',
    version='0.1.0',
    url='https://github.com/yanqingmen/ask-api',
    license="Apache License 2.0",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='yanqingmen',
    python_requires='>=3.7',
    install_requires=requirements,
    package_dir={"": "src"},
    packages=pkgs,
)
