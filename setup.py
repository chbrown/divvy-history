from setuptools import setup

setup(
    name='divvy',
    version='0.0.5',
    packages=['divvy'],
    install_requires=[
        'apscheduler',
        'jsonpatch',
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'divvy = divvy.cli:main',
        ],
    },
)
