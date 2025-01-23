from setuptools import setup, find_packages

setup(
    name='bitscrunch_unleashnftV2_sdk',
    version='0.1.12',
    description='A Python SDK for interacting with the bitsCrunch API V2',
    author='Anupama',
    author_email='anupamarawat71@gmail.com',
    packages=find_packages(),
    install_requires=[
        'requests'
    ],
)
