# setup.py

from setuptools import setup, find_packages

setup(
    name='sankalp',
    version='1.2.6',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "sankalp": ["blue.mp3"],
    },
    install_requires=[
        'curses; platform_system!="Windows"',
        'windows-curses; platform_system=="Windows"',
        'rich',
        'PyInquirer',
        "pygame"
    ],
    entry_points={
        'console_scripts': [
            'sankalp = sankalp.cli:run_cli',
        ],
    },
    python_requires='>=3.6',
    author='Sankalp Shrivastava',
    author_email='s@sankalp.sh',
    description='A simple CLI package for Sankalp Shrivastava',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/1sankalp',
)
