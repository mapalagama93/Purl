from setuptools import setup

setup(
    name='purl',
        version='0.1.0',
        install_requires=[
            'Faker',
            'jproperties',
            'jsonpath_ng',
            'PyYAML',
            'PyYAML',
            'Requests',
            'requests_toolbelt',
            'termcolor'
        ],
        entry_points={
            'console_scripts': [
                'purl = app:main',
            ],
        }
    )
