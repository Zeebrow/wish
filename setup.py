from setuptools import setup

setup(
    name='wish',
    version='0.0.1',
    py_modules=[''],
    install_requires=[
        'Click',
        'GitPython'
    ],
    entry_points={
        'console_script': [
            'wish = main:cli',
        ],
    },
)
