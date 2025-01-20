from setuptools import setup, find_packages
import os


def _load_famegui_version():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    init_filepath = os.path.join(this_dir, "famegui", "__init__.py")

    with open(init_filepath) as f:
        for line in f.readlines():
            if line.startswith("__version__"):
                delim = '"' if '"' in line else "'"
                return line.split(delim)[1]
    raise RuntimeError("Unable to find version string in {}".format(init_filepath))


def _readme():
    with open("README.md") as f:
        return f.read()


VERSION = _load_famegui_version()

setup(
    name="famegui",
    packages=find_packages(),
    version=VERSION,
    keywords=["FAME", "agent-based modelling"],
    license="Apache License 2.0",
    description="Graphical user interface to the FAME modelling framework",
    long_description=_readme(),
    long_description_content_type="text/markdown",
    author="Aurélien Regat-Barrel, Simon Wischnevetski",
    author_email="fame@dlr.de",

    url="https://gitlab.com/fame-framework/FAME-Gui",
    download_url="https://gitlab.com/fame-framework/FAME-Gui/-/archive/v{}/FAME-Gui-v{}.tar.gz".format(
        VERSION, VERSION
    ),
    install_requires=[
        "coloredlogs",
        "fameio>=3.0",
        "python-igraph",
        "pyyaml",
        "ipython",
        "PySide6",
        "SQLAlchemy>=1.4.44",
        "pytest==8.3.4",
        "matplotlib",
        "ujson",
        "icecream",
    ],
    python_requires=">=3.9",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Visualization",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    entry_points={
        "console_scripts": [
            "famegui=famegui.app:main",
        ],
    },
    package_data={
        "famegui": ["data/*", "database/database.sqlite3", "*sqlite3"],
    },
    include_package_data=True,
)
