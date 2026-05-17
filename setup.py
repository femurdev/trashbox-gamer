"""
Setup script for Trashbox Gamer
"""
from setuptools import setup, find_packages

setup(
    name="trashbox-gamer",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'pygame>=2.5.0',
        'pillow>=10.0.0',
        'numpy>=1.24.0',
    ],
    extras_require={
        'dev': [
            'black',
            'flake8',
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'trashbox-gamer=main:main',
        ],
    },
    python_requires='>=3.8',
)
