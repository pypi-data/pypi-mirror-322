from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.1'
DESCRIPTION = 'GPC data analysis'
LONG_DESCRIPTION = 'Python package for the analysis of gel permeation chromatography (GPC) data.'

# Setting up
setup(
    name="polymertools",
    version=VERSION,
    author="heisenbergpxh (Fabian Hofmann)",
    author_email="<hofmann.fa@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['numpy', 'scipy', 'matplotlib'],
    keywords=['python', 'data analysis', 'polymer', 'deconvolution'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)