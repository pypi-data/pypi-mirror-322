from setuptools import setup, find_packages

setup(
    name='fantomcryptor',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'cryptography',
    ],
    description='A custom encryption algorithm combining Fernet, AES 256 GCM, RSA, and Vigenère Cipher.',
    author='Your Name',
    author_email='your.email@example.com',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)
