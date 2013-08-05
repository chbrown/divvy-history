from setuptools import setup

setup(
    name='divvy',
    version='0.0.4',
    packages=['divvy'],
    install_requires=[
        'jsonpatch',
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'divvy-fetch = divvy.fetch:main',
            'divvy-sync = divvy.sync:main',
        ],
    },
)
