from setuptools import setup, find_packages

setup(
    name='Command Line Utils',
    packages=find_packages(include=['crud.base']),
    entry_points={
        'console_scripts': [
            'seed_db=crud.base:seed_db',
        ],
    }
)
