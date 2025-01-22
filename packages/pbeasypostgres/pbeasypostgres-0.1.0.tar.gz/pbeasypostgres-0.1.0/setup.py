from setuptools import setup, find_packages

setup(
    name='pbeasypostgres',
    version='0.1.0',
    author='ig-acc',
    author_email='igortalin8@gmail.com',
    description='Easy PostgreSQL database adapter for Python based on psycopg2',
    packages=find_packages(),
    install_requires=[
        "psycopg2"
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
)