
from setuptools import setup, find_packages

setup(
    name='dasty_api',
    version='0.2.6',
    author='Rohit Singh',
    author_email='rsingh.yaml@gmail.com',
    description='Declarative API Scenario Testing in YAML - Easily define and run API tests using YAML.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/rohitkochhar/dasty',
    packages=find_packages(),
    install_requires=[
        'certifi==2023.11.17',
        'charset-normalizer==3.3.2',
        'idna==3.6',
        'PyYAML==6.0.1',
        'requests==2.31.0',
        'urllib3==2.1.0'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
