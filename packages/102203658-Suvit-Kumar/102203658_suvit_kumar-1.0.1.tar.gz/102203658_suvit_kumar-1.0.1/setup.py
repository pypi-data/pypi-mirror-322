from setuptools import setup, find_packages

setup(
    name='102203658_Suvit_Kumar',
    version='1.0.1',
    author='Suvit Kumar',
    author_email='skumar5_be22@thapr.edu',
    description='A package for TOPSIS multi-criteria decision making',
    packages=find_packages(),
    install_requires=['numpy', 'pandas'],
    entry_points={
        'console_scripts': [
            'topsis=topsis.topsis:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
