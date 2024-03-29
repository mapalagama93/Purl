from setuptools import setup

setup(
    name='purl',
        version='0.1.0',
        install_requires=[
            'requests',
            'termcolor',
            'jsonpath-ng',
            'pyyaml',
            'requests_toolbelt',
            'jproperties'
        ],
        entry_points={
            'console_scripts': [
                'purl = app:main',
            ],
        }
    )
