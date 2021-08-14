from setuptools import setup, find_packages

setup(
    name='wish',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        'Click',
        'GitPython'
    ],
    entry_points={
        'console_scripts': [
            'wish = main:cli',
        ],
    },
)
