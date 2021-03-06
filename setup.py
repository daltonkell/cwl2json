import os
from setuptools import setup, find_packages

# TODO versioneer?

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

# define the actual command-line tool that will be callable
console_scripts = []
version = '0.0.1'
# minimal depedencies
requires = ['pyyaml']
# additional data needed
pkg_data = {}

setup(
    name = "cwl2json",
    version = version,
    author = "Dalton Kell",
    author_email = "dalton.kell@rpsgroup.com",
    description = ("A simple tool to launch and manage HPC clusters."),
    packages = find_packages(),
    install_requires = requires,
    entry_points=dict(console_scripts=console_scripts),
    include_package_data = True,
    zip_safe = False,
    package_data = pkg_data,
    long_description=read('README.md'),
    classifiers=[
    #     "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Programming Language :: Python",
        "Topic :: Scientific/Engineering",
        # "License :: OSI Approved :: Apache Software License",
    ],
)

