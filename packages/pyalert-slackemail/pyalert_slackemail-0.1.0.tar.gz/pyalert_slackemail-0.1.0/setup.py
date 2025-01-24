# tests/test_logger.py

from logging_slack_email.logger import Logger
from setuptools import setup, find_packages

setup(
    name='pyalert-slackemail',
    version='0.1.0',
    author='Vaibhav Kharatmal',
    author_email='vaibhav.kharatmal@shreemaruti.com',
    description='A Package for creating default logs and posting logs to slack and email',
    packages=find_packages(),
    install_requires=[
        # List your package dependencies here
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)