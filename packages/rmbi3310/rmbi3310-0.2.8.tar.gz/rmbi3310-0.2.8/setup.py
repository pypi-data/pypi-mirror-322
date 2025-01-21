from setuptools import setup, find_packages

setup(
    name='rmbi3310',
    version='0.2.8',
    description='Do not distribute it without permission. ',
    author='Xuhu Wan',
    author_email='xuhu.wan@gmail.com',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        'plotly',
        'yfinance',
        'statsmodels'
    ],
)
