from setuptools import setup, find_packages

setup(
    name='mymathpack',  # Name of the package
    version='0.1',  # Version of the package
    description='A simple math library with addition functionality.',
    author='Your Name',
    author_email='your.email@example.com',
    packages=find_packages(),  # Automatically find packages in the directory
    install_requires=[],  # List dependencies here if needed
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Minimum Python version
)
