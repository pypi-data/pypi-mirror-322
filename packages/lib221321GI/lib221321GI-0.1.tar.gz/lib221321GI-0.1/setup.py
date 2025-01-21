from setuptools import setup, find_packages

setup(
    name='lib221321GI',
    version='0.1',
    packages=find_packages(),
    install_requires=['psycopg2'],
    author='Sidezi',
    author_email='gus3viw@yandex.ru',
    description='A library for interacting with a PostgreSQL database',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)