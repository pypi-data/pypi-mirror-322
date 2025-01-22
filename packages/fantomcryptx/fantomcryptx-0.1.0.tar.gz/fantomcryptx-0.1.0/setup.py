# setup.py
from setuptools import setup, find_packages

setup(
    name="fantomcryptx",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        'cryptography',
        'pycryptodome'
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="FantomCRYPT: A custom cryptographic algorithm combining AES, RSA, and Vigenère.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
