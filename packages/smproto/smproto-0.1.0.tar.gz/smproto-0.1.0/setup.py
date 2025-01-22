from setuptools import setup, find_packages

setup(
    name='smproto',  # Name of your package
    version='0.1.0',  # Version of your package
    packages=find_packages(),  # Automatically find your package
    description='A secure messaging protocol using ECDSA and ECDH',
    long_description=open('README.md').read(),  # Long description from README file
    long_description_content_type='text/markdown',  # Content type for the description
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/yourusername/smproto',  # Repository URL
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=[
        'cryptography',  # Add any dependencies here
    ],
)
