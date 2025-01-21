from setuptools import setup

setup(
    name='aes-encryption-tool',  # Your package name
    version='1.0.1',             # Version of your tool
    py_modules=['aes_encryption_tool'],    # List your single Python file
    install_requires=[
        'PyQt5',
        'cryptography',
    ],
    entry_points={
        'console_scripts': [
            'aes-tool=aes_encryption_tool:main',  # Command to run your tool
        ],
    },
    description='AES Encryption/Decryption Tool with PyQt5 GUI',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='SYED AHNAF RAZA',
    author_email='syahra2014@gmail.com',
    url='https://github.com/syahra712/aes-encryption',  # Optional GitHub link
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)
