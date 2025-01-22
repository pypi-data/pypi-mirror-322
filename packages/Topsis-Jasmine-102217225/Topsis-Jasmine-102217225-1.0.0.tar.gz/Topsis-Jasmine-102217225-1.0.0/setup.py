from setuptools import setup, find_packages

setup(
    name="Topsis-Jasmine-102217225",
    version="1.0.0",
    author="Jasmine Kaur",
    author_email="jkaur3_be22@thapar.edu",
    description="A Python package to implement the TOPSIS method.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/kjasmine-git/Topsis-Jasmine-102217225",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "pandas"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'topsis=topsis.topsis:main',
        ],
    },
    python_requires=">=3.6",
)
