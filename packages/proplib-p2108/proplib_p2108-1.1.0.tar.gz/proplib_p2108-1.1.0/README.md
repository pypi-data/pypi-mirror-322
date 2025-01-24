# Recommendation ITU-R P.2108 - Python® Wrapper #

[![NTIA/ITS PropLib][proplib-badge]][proplib-link]
[![PyPI Release][pypi-release-badge]][pypi-release-link]
[![GitHub Actions Unit Test Status][gh-actions-test-badge]][gh-actions-test-link]
[![GitHub Issues][gh-issues-badge]][gh-issues-link]
[![DOI][doi-badge]][doi-link]

[proplib-badge]: https://img.shields.io/badge/PropLib-badge?label=%F0%9F%87%BA%F0%9F%87%B8%20NTIA%2FITS&labelColor=162E51&color=D63E04
[proplib-link]: https://ntia.github.io/propagation-library-wiki
[gh-actions-test-badge]: https://img.shields.io/github/actions/workflow/status/NTIA/p2108-python/pytest.yml?branch=main&logo=pytest&logoColor=ffffff&label=Tests&labelColor=162E51
[gh-actions-test-link]: https://github.com/NTIA/p2108-python/actions/workflows/pytest.yml
[pypi-release-badge]: https://img.shields.io/pypi/v/proplib-p2108?logo=pypi&logoColor=ffffff&label=Release&labelColor=162E51&color=D63E04
[pypi-release-link]: https://pypi.org/project/proplib-p2108
[gh-issues-badge]: https://img.shields.io/github/issues/NTIA/p2108-python?logo=github&label=Issues&labelColor=162E51
[gh-issues-link]: https://github.com/NTIA/p2108-python/issues
[doi-badge]: https://zenodo.org/badge/804561453.svg
[doi-link]: https://zenodo.org/badge/latestdoi/804561453

This repository contains a Python wrapper for the NTIA/ITS implementation of
Recommendation ITU-R P.2108. This Recommendation contains three methods for the
prediction of clutter loss: Height Gain Terminal Correction Model, Terrestrial
Statistical Model, and Aeronautical Statistical Model. The software implements
Section 3 of Annex 1 of the Recommendation. This Python package wraps the
[NTIA/ITS C++ implementation](https://github.com/NTIA/p2108).

## Getting Started ##

This software is distributed on [PyPI](https://pypi.org/project/proplib-p2108) and is easily installable
using the following command.

```cmd
pip install proplib-p2108
```

General information about using this model is available on
[its page on the **NTIA/ITS Propagation Library Wiki**](https://ntia.github.io/propagation-library-wiki/models/P2108/).
Additionally, Python-specific instructions and code examples are available
[here](https://ntia.github.io/propagation-library-wiki/models/P2108/python).

If you're a developer and would like to contribute to or extend this repository,
please review the guide for contributors [here](CONTRIBUTING.md) or open an
[issue](https://github.com/NTIA/p2108-python/issues) to start a discussion.

## Development ##

This repository contains code which wraps [the C++ shared library](https://github.com/NTIA/p2108)
as an importable Python module. If you wish to contribute to this repository,
testing your changes will require the inclusion of this shared library. You may retrieve
this either from the
[relevant GitHub Releases page](https://github.com/NTIA/p2108/releases), or by
compiling it yourself from the C++ source code. Either way, ensure that the shared library
(`.dll`, `.dylib`, or `.so` file) is placed in `src/ITS/ITU/PSeries/P2108/`, alongside `__init__.py`.

Below are the steps to build and install the Python package from the source code.
Working installations of Git and a [currently-supported version](https://devguide.python.org/versions/)
of Python are required. Additional requirements exist if you want to compile the shared
library from C++ source code; see relevant build instructions
[here](https://github.com/NTIA/p2108?tab=readme-ov-file#configure-and-build).

1. Optionally, configure and activate a virtual environment using a tool such as
[`venv`](https://docs.python.org/3/library/venv.html) or
[conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html).

1. Clone this repository, then initialize the Git submodule containing the test data.

    ```cmd
    # Clone the repository
    git clone https://github.com/NTIA/p2108-python
    cd p2108-python

    # Initialize Git submodule containing test data
    git submodule init

    # Clone the submodule
    git submodule update
    ```

1. Download the shared library (`.dll`, `.so`, or `.dylib`) from a
[GitHub Release](https://github.com/NTIA/p2108/releases). Then place the
downloaded file in `src/ITS/ITU/PSeries/P2108/` (alongside `__init__.py`).

1. Install the local package and development dependencies into your current environment:

    ```cmd
    pip install .[dev]
    ```

1. To build the wheel for your platform:

    ```cmd
    hatchling build
    ```

### Running Tests ###

Python unit tests can be run to confirm successful installation. You will need to
clone this repository's test data submodule (as described above). Then, run the tests
with pytest using the following command.

```cmd
pytest
```

Additionally, the [Study Group Clutter Excel Workbook](https://www.itu.int/en/ITU-R/study-groups/rsg3/ionotropospheric/Clutter%20and%20BEL%20workbook_V2.xlsx)
contains an extensive set of example values which are useful as validation cases.

## References ##

- [ITS Propagation Library Wiki](https://ntia.github.io/propagation-library-wiki)
- [P2108 Wiki Page](https://ntia.github.io/propagation-library-wiki/models/P2108)
- [`ITS.ITU.PSeries.P2108` C++ API Reference](https://ntia.github.io/P2108)
- [Recommendation ITU-R P.2108](https://www.itu.int/rec/R-REC-P.2108/en)
- [Report ITU-R P.2402](https://www.itu.int/pub/R-REP-P.2402)

## License ##

See [LICENSE](./LICENSE.md).

"Python" and the Python logos are trademarks or registered trademarks of the Python Software Foundation, used by the National Telecommunications and Information Administration with permission from the Foundation.

## Contact ##

For technical questions, contact <code@ntia.gov>.

## Disclaimer ##

Certain commercial equipment, instruments, or materials are identified in this project were used for the convenience of the developers. In no case does such identification imply recommendation or endorsement by the National Telecommunications and Information Administration, nor does it imply that the material or equipment identified is necessarily the best available for the purpose.
