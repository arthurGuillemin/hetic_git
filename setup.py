from setuptools import setup, find_packages

setup(
    name='mygit',
    version='0.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'mygit = gitfs.main:main',
        ],
    },
)
