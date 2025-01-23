from setuptools import setup, find_packages

setup(
    name="partisan_cat",
    version="0.1.0",
    description="A comprehensive toolset for data management, hashing operations, JSON conversions, and more.",
    author="Abbas Faramarzi Filabadi",
    author_email="abbasfaramarzi068@gmail.com",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        # Remove 'os', 'json', 'logging', 'copy', 'hashlib', 'datetime'
        # Add any third-party dependencies here
        # example: "numpy>=1.21.2"
    ],
    python_requires='>=3.7',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
)
