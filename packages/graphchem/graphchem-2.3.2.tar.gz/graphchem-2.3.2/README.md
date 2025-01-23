[![UML Energy & Combustion Research Laboratory](https://sites.uml.edu/hunter-mack/files/2021/11/ECRL_final.png)](http://faculty.uml.edu/Hunter_Mack/)

# GraphChem: Graph-based machine learning for chemical property prediction

[![GitHub version](https://badge.fury.io/gh/ecrl%2FGraphChem.svg)](https://badge.fury.io/gh/ecrl%2FGraphChem)
[![PyPI version](https://badge.fury.io/py/graphchem.svg)](https://badge.fury.io/py/graphchem)
[![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](https://raw.githubusercontent.com/ecrl/GraphChem/master/LICENSE.txt)
[![Documentation Status](https://readthedocs.org/projects/graphchem/badge/?version=latest)](https://graphchem.readthedocs.io/en/latest/?badge=latest)

**GraphChem** is an open source Python package for constructing graph-based machine learning models with a focus on fuel property prediction.

# Installation:

### Prerequisites:
- Have Python 3.11+ installed

### Method 1: pip
```
$ pip install graphchem
```

### Method 2: From Source
```
$ git clone https://github.com/ecrl/graphchem
$ cd graphchem
$ python -m pip install .
```

If any errors occur when installing dependencies, namely with RDKit, PyTorch, or torch-geometric, visit their installation pages and follow the installation instructions: [RDKit](https://www.rdkit.org/docs/Install.html), [PyTorch](https://pytorch.org/get-started/locally/), [PyTorch Geometric](https://pytorch-geometric.readthedocs.io/en/latest/notes/installation.html)

# Usage:

For advanced usage, head over to our [API documentation page](https://graphchem.readthedocs.io/en/latest/).

# Examples

To view some examples of how GraphChem can be used, head over to our [examples](https://github.com/ecrl/graphchem/tree/master/examples) folder on GitHub.

# Contributing, Reporting Issues and Other Support:

To contribute to GraphChem, make a pull request. Contributions should include tests for new features added, as well as extensive documentation.

To report problems with the software or feature requests, file an issue. When reporting problems, include information such as error messages, your OS/environment and Python version.

For additional support/questions, contact Travis Kessler (Travis_Kessler@student.uml.edu).
