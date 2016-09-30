'''setup.py for slack-archiver'''
from setuptools import setup, find_packages
import versioneer

setup(
    name='slack-archiver',
    cmdclass=versioneer.get_cmdclass(),
    version=versioneer.get_version(),
    description='Archives slack channels',
    author='Mike Bryant',
    author_email='mike.bryant@ocado.com',
    packages=find_packages(),
    install_requires=[
        'ConfigArgParse <= 0.11.0, < 1.0.0',
        'slacker',
    ],
    entry_points={
        'console_scripts': [
            'slack-archiver = slack_archiver.__main__:main'
        ]
    },
)
