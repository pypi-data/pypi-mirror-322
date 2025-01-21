from setuptools import setup, find_packages

VERSION = "1.0.2"
DESCRIPTION = " A command line file organizer made. My largest project so far."
with open("README.md") as file:
    LONG_DESCRIPTION = file.read()

setup(
    name = "claire_organizer",
    version = VERSION,
    author = "Zizel",
    author_email = "danbua999@gmail.com",
    description = DESCRIPTION,
    long_description = LONG_DESCRIPTION,
    long_description_content_type = "text/markdown",
    url = "https://github.com/uwungu01-rep/claire_organizer-python.edition",
    packages = find_packages(),
    install_requires = [], # add any additional packages that 
    # needs to be installed along with your package. Eg: "caer"
    classifiers = [
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
    entry_points = {
        "console_scripts": [
            "elford  = claire_organizer.main:main",
        ],
    },
)