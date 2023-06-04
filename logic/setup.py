from setuptools import setup, find_packages

setup(
    name='Command Line Utils',
    packages=find_packages(include=['crud.base', 'logic.elastic_cli']),
    entry_points={
        'console_scripts': [
            'seed_db=crud.base:seed_db',
            'tag_count=crud.tag:get_tag_from_console',
            'create_index=logic.elastic_search:create_index'
        ],
    }
)
