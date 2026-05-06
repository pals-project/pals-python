# Meet Your Python PALS

This is a Python implementation for the Particle Accelerator Language Standard ([PALS](https://github.com/campa-consortium/pals)).

To define the PALS schema, [Pydantic](https://docs.pydantic.dev) is used to map to Python objects, perform automatic validation, and serialize/deserialize data classes to/from many modern file formats.
Various modern file formats (e.g., YAML, JSON, TOML, XML, etc.) are supported, which makes the implementation of the schema-following files in any modern programming language easy (e.g., Python, Julia, C++, LUA, Javascript, etc.).
Here, we do Python.


## Status

This project is a work-in-progress and evolves alongside the Particle Accelerator Language Standard ([PALS](https://github.com/campa-consortium/pals)).


## Approach

This project implements the PALS schema in a file-agnostic way, mirrored in data objects.
The corresponding serialized files (and optionally, also the corresponding Python objects) can be human-written, human-read, and automatically validated.

PALS files follow a schema and readers can error out on issues.
Not every PALS implementation needs to be as detailed as the reference implementation in Python.
This implementation can be used to convert between different file formats or to validate a file before reading it with your favorite YAML/JSON/TOML/XML/... library in your programming language of choice.

This will enable us to:
- exchange lattices between codes;
- use common GUIs for defining lattices;
- use common lattice visualization tools (2D, 3D, etc.).


### FAQ

*Why use Pydantic for this implementation?*  
Implementing directly against a specific file format is possible, but cumbersome.
By using a widely-used schema engine, such as [Pydantic](https://docs.pydantic.dev), we can get serialization/deserialization to/from various file formats, conversion, and validation "for free".


## Roadmap

Preliminary roadmap:

1. Define the PALS schema, using Pydantic.
2. Document the API.
3. Develop a reference implementation in Python. Attract additional reference implementations in other languages.
5. Add supporting helpers, which can import existing MAD-X, Elegant, SXF files. Be as feature complete as possible in these importers.
6. Reuse the reference implementations and implement readers in community codes for beamline modeling (e.g., the [BLAST codes](https://blast.lbl.gov)).


## For users

You can install this Python implementation of PALS via ``pip install pals-schema``. Package releases can be found [here](https://pypi.org/project/pals-schema/).

Once installed, you can run the examples available in the [examples](https://github.com/campa-consortium/pals-python/tree/main/examples) directory to verify that the package was installed correctly.

If you wish to run the unit tests available in the [tests](https://github.com/campa-consortium/pals-python/tree/main/tests) directory, please install the package via ``pip install pals-schema[test]`` to make sure that all additional dependencies (e.g., ``pytest``) are installed correctly.

## For developers

In order to develop and test this Python implementation locally, please follow these steps:

1. Create a conda environment from the `environment.yml` file:
    ```bash
    conda env create -f environment.yml
    ```
2. Activate the conda environment:
    ```bash
    conda activate pals-python
    ```
   (This is the environment name in the `environment.yml` file.)
3. Install Python PALS in development (editable) mode:
    ```bash
    pip install -e ".[test]"
    ```

Once you have created the environment with all the required dependencies, you can run the examples available in the [examples](https://github.com/campa-consortium/pals-python/tree/main/examples) directory.

You can also run the unit tests available in the [tests](https://github.com/campa-consortium/pals-python/tree/main/tests) directory via
```bash
pytest tests -v
```
Here, the command line option `-v` increases the verbosity of the output.
You can also use the command line option `-s` to display any test output directly in the console (useful for debugging).
Please refer to [pytest's documentation](https://docs.pytest.org/en/stable/) for further details on the available command line options and/or run `pytest --help`.

## Copyright Notice and License Agreement

PALS Python Copyright (c) 2025, The Regents of the University of California,
through Lawrence Berkeley National Laboratory (subject to receipt of
any required approvals from the U.S. Dept. of Energy). All rights reserved.

If you have questions about your rights to use or distribute this software,
please contact Berkeley Lab's Intellectual Property Office at
IPO@lbl.gov.

Please find the full copyright notice in [NOTICE.txt](NOTICE.txt) and the full license agreement in [LICENSE.txt](LICENSE.txt).

The SPDX license identifier is `BSD-3-Clause-LBNL`.
