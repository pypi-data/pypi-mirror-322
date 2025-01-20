[![PyPI version](https://badge.fury.io/py/famegui.svg)](https://badge.fury.io/py/famegui)
[![PyPI license](https://img.shields.io/pypi/l/famegui.svg)](https://badge.fury.io/py/famegui)
[![pipeline status](https://gitlab.com/fame-framework/FAME-Gui/badges/main/pipeline.svg)](https://gitlab.com/fame-framework/FAME-Gui/commits/main)
[![coverage report](https://gitlab.com/fame-framework/FAME-Gui/badges/main/coverage.svg)](https://gitlab.com/fame-framework/FAME-Gui/-/commits/main) 

# FAME-Gui
FAME-Gui is a graphical user interface for [FAME](https://helmholtz.software/software/fame) models.
Please visit the [FAME-Wiki](https://gitlab.com/fame-framework/fame-wiki/-/wikis/home) to get an explanation of FAME and its components or read the accompanying papers about [FAME-Core](https://doi.org/10.21105/joss.05087) and [FAME-Io](https://doi.org/10.21105/joss.04958).
    
FAME-Gui is currently under development, see [milestones](https://gitlab.com/fame-framework/FAME-Gui/-/milestones) and [issues](https://gitlab.com/fame-framework/fame-gui/-/issues).

# Installation

    pip install famegui

You may also use `pipx`. For detailed information please refer to the official `pipx` [documentation](https://github.com/pypa/pipx).

    pipx install famegui


# Usage
FAME-Gui is started in the console using

    famegui

# Contribute
Please read the Contributors License Agreement `cla.md`, sign it and send it to [`fame@dlr.de`](mailto:fame@dlr.de) before contributing.

## Testing changes locally

Once some changes have been performed on the local git clone, use the following command to override your local installation with your modified copy in order to test the result:

```bash
python3 setup.py bdist_wheel && pip3 install --force-reinstall --no-dependencies ./dist/*.whl
```

## Code style

We use the code formatting library [`black`](https://pypi.org/project/black/).
The maximum line length is defined as 120 characters. 
Therefore, before committing, run `black --line-length 120 .`.
