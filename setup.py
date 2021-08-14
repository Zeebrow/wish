from setuptools import setup

setup(
    name='prospector',
    version='0.0.1',
    py_modules=[''],
    install_requires=[
        'Click',
        'GitPython'
    ],
    entry_points={
        'console_script': [
            'wish = main_cmd:cli',
        ],
    },
)