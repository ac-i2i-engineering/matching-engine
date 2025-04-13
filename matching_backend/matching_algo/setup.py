from setuptools import setup, find_packages

setup(
    name="matching_algo",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'django',
        'sphinx',
        'sphinx-autodoc-typehints',
        'pandas',
        'numpy',
        'django-environ',  # for handling environment variables
    ],
)