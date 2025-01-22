from setuptools import setup, find_packages
from pathlib import Path

long_description = Path('README.md').read_text()

setup(
    name='hoyowrapper',
    version='0.1.2',
    packages=find_packages(include=['hoyowrapper']),
    author='Guitarband',
    author_email='preetish_choudhary@outlook.com',
    description='A library for handling interactions with Hoyolab via Python.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=['requests', 'asyncio', 'pyppeteer'],
    setup_requires=[],
    tests_require=[],
    test_suite='tests'
)