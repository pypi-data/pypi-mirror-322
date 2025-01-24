import os
from setuptools import find_packages, setup

#Metadata of package

NAME = 'Loanapp'
DESCRIPTION = 'Loanapp_prediction_model'
URL = 'https://github.com/aicouncil'
EMAIL = 'info@aicouncil.in'
AUTHOR = 'Aicouncil'
REQUIRES_PYTHON = '>=3.7.0'

pwd = os.path.abspath(os.path.dirname(__file__))
#print(pwd)

#get the list of packages to be installed
def list_reqs(fname = 'requirements.txt'):
    with open(os.path.join(pwd,fname)) as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]
    
# Read the README file
try:
    with open(os.path.join(pwd, 'README.md'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

#Load the packages's version 
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
PACKAGE_DIR = os.path.join(ROOT_DIR, NAME)
#print(PACKAGE_DIR)


about = {}
try:
    with open(os.path.join(PACKAGE_DIR, 'VERSION')) as f:
        about['__version__'] = f.read().strip()
except FileNotFoundError:
    raise RuntimeError("VERSION file not found. Ensure it exists in the package directory.")


setup(
    name=NAME,
    version=about['__version__'],
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(exclude=('tests',)),
    package_data={'loanapp_prediction_model': ['VERSION']},
    install_requires=list_reqs(),
    extras_require={},
    include_package_data=True,
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
)
