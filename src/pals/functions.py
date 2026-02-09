"""Public, free-standing functions for PALS."""

import os


def inspect_file_extensions(filename: str):
    """Attempt to strip two levels of file extensions to determine the schema.

    filename examples: fodo.pals.yaml, fodo.pals.json, ...
    """
    file_noext, extension = os.path.splitext(filename)
    file_noext_noext, extension_inner = os.path.splitext(file_noext)

    if extension_inner != ".pals":
        raise RuntimeError(
            f"inspect_file_extensions: No support for file {filename} with extension {extension}. "
            f"PALS files must end in .pals.json or .pals.yaml or similar."
        )

    return {
        "file_noext": file_noext,
        "extension": extension,
        "file_noext_noext": file_noext_noext,
        "extension_inner": extension_inner,
    }


def load_file_to_dict(filename: str) -> dict:
    # Attempt to strip two levels of file extensions to determine the schema.
    #   Examples: fodo.pals.yaml, fodo.pals.json, ...
    file_noext, extension, file_noext_noext, extension_inner = inspect_file_extensions(
        filename
    ).values()

    # examples: fodo.pals.yaml, fodo.pals.json
    with open(filename, "r") as file:
        if extension == ".json":
            import json

            pals_data = json.loads(file.read())

        elif extension == ".yaml":
            import yaml

            pals_data = yaml.safe_load(file)

        # TODO: toml, xml

        else:
            raise RuntimeError(
                f"load_file_to_dict: No support for PALS file {filename} with extension {extension} yet."
            )

    return pals_data


def store_dict_to_file(filename: str, pals_dict: dict):
    file_noext, extension, file_noext_noext, extension_inner = inspect_file_extensions(
        filename
    ).values()

    # examples: fodo.pals.yaml, fodo.pals.json
    if extension == ".json":
        import json

        json_data = json.dumps(pals_dict, sort_keys=True, indent=2)
        with open(filename, "w") as file:
            file.write(json_data)

    elif extension == ".yaml":
        import yaml

        yaml_data = yaml.dump(pals_dict, default_flow_style=False)
        with open(filename, "w") as file:
            file.write(yaml_data)

    # TODO: toml, xml

    else:
        raise RuntimeError(
            f"store_dict_to_file: No support for PALS file {filename} with extension {extension} yet."
        )
