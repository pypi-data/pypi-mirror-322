from setuptools import setup, find_packages

setup(
    name='xuiniaDB',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'portableDB',
        'pydub',
        'colorama',
        'opencv-python'
    ],

)