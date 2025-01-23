from setuptools import setup, find_packages
import os

here = os.path.abspath(os.path.dirname(__file__))



VERSION = '0.0.1'
DESCRIPTION = 'Just a package that make python easier and simple, and its add few packages in 1, like files and more'


# Setting up
setup(
    name="NR_Python",
    version=VERSION,
    author="NR_5tudio",

    description=DESCRIPTION,


    packages=find_packages(),
    install_requires=['mouse', 'keyboard'],
    keywords=['Python', 'Simple', 'easy', 'File', 'time', 'short', 'shortcuts'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows"
    ]
)