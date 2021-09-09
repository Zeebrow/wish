from setuptools import setup, find_packages

setup(
    # pip install -e . / pip uninstal -y wish
    name='wish',
    version='0.0.1',
    package_dir={'': 'src'},
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

