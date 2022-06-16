from setuptools import setup

import coingecko


def readme():
    '''Read README file'''
    with open('README.rst') as file:
        return file.read()


setup(
    name='coingecko',
    version=coingecko.__version__,
    description='Python API wrapper for https://coingeckeo.com',
    long_description=readme().strip(),
    author='',
    author_email='',
    url='https://github.com/trycoast/coingecko',
    license='MIT',
    packages=['coingecko'],
    install_requires=['requests', 'tenacity', 'ratelimit @ git+https://github.com/trycoast/ratelimit.git'],
    keywords=[
        'api',
        'coingecko',
        'aggregator',
        'crypto'
    ],
    include_package_data=True,
    zip_safe=False
)
