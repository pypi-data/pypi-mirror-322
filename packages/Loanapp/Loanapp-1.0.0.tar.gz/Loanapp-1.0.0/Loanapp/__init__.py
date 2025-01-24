import os

PACKAGE_ROOT = os.path.dirname(os.path.abspath(__file__))
#print(PACKAGE_ROOT)

with open(os.path.join(PACKAGE_ROOT,'VERSION')) as f:
    __version__ = f.read().strip()
    #print(__version__)