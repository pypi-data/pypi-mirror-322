from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setup (
    name='de_embedding_rf',
    version='0.1.2',
    license='MIT',
    description='methods for de-embedding process: T-R-L, L-L and T-VR-L',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author= 'Aplata',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'de-embedding': ['data/raw/simulation_ADS/*.s1p'],
        'de-embedding': ['data/raw/simulation_ADS/*.s2p'],
    },
    install_requires = ['numpy','pandas','scikit-rf','matplotlib','scipy'],

    url='https://github.com/aplatag/project_SL_regression_quality.git'
)