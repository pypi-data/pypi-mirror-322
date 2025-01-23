import os
from datetime import datetime

from setuptools import setup, find_packages

version = os.environ['PACKAGE_VERSION']

setup(
    name='tui_dsg',
    version=version,
    author='Eric Tröbs',
    author_email='eric.troebs@tu-ilmenau.de',
    description='everything you need for our jupyter notebooks',
    long_description='everything you need for our jupyter notebooks',
    long_description_content_type='text/markdown',
    url='https://dbgit.prakinf.tu-ilmenau.de/lectures/data-science-grundlagen',
    project_urls={},
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    python_requires='>=3.10',
    install_requires=[
        'jupyter',
        'ipywidgets',
        'checkmarkandcross',
        'beautifulsoup4==4.12.3',
        'fa2_modified==0.3.10',
        'grizzly_sql==0.1.5.post1',  # newer grizzly versions require additional dependencies!
        'HanTa==1.1.1',
        'kaleido~=0.2.1',
        'Levenshtein==0.26.1',
        'matplotlib==3.9.4',
        'networkx==3.4.2',
        'nltk==3.9.1',
        'numpy==1.26.4',  # spaCy does not work with NumPy>=2.0.0 atm
        'pandas==2.2.3',
        'pillow==11.0.0',
        'plotly==5.24.1',
        'pyyaml==6.0.2',
        'requests==2.32.3',
        'scikit-learn==1.6.0',
        'scipy==1.14.1',
        'spacy==3.7.5',
        'statsmodels==0.14.4',
        'torch==2.5.1'  # See also Dockerfile for torch dependency!
    ],
    package_data={
        'tui_dsg': [
            'datasets/resources/*',
        ]
    },
    include_package_data=True
)
