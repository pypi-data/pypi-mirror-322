from setuptools import setup, find_packages

setup(
    name="FantomCRYPT",
    version="1.0.0",
    packages=find_packages(),
    description="A custom encryption library combining multiple ciphers",
    install_requires=[
        'cryptography',
        'pycryptodome',
    ],
)
