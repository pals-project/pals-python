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


def _numpy_to_native(obj):
    """Convert a numpy scalar/array to its Python-native equivalent.

    Returns ``None`` when the object is not a numpy type or when numpy is not
    installed; callers use that to decide whether to fall back to the default
    serializer behavior. numpy is an optional dependency.
    """
    try:
        import numpy as np
    except ImportError:
        return None

    if isinstance(obj, np.ndarray):
        return obj.tolist()
    if isinstance(obj, np.generic):
        return obj.item()
    return None


def store_dict_to_file(filename: str, pals_dict: dict):
    file_noext, extension, file_noext_noext, extension_inner = inspect_file_extensions(
        filename
    ).values()

    # examples: fodo.pals.yaml, fodo.pals.json
    if extension == ".json":
        import json

        def _json_default(obj):
            native = _numpy_to_native(obj)
            if native is not None:
                return native
            raise TypeError(
                f"Object of type {type(obj).__name__} is not JSON serializable"
            )

        json_data = json.dumps(
            pals_dict, sort_keys=False, indent=2, default=_json_default
        )
        with open(filename, "w") as file:
            file.write(json_data)

    elif extension == ".yaml":
        import yaml

        # Subclass the safe dumper so numpy representers are scoped to PALS
        # serialization and do not leak into the global pyyaml state used by
        # other code in the same process.
        class _PALSDumper(yaml.SafeDumper):
            pass

        try:
            import numpy as np
        except ImportError:
            np = None

        if np is not None:

            def _represent_numpy_scalar(dumper, value):
                native = value.item()
                if isinstance(native, bool):
                    return dumper.represent_bool(native)
                if isinstance(native, int):
                    return dumper.represent_int(native)
                if isinstance(native, float):
                    return dumper.represent_float(native)
                return dumper.represent_data(native)

            def _represent_numpy_array(dumper, value):
                return dumper.represent_list(value.tolist())

            _PALSDumper.add_multi_representer(np.generic, _represent_numpy_scalar)
            _PALSDumper.add_representer(np.ndarray, _represent_numpy_array)

        yaml_data = yaml.dump(
            pals_dict,
            Dumper=_PALSDumper,
            default_flow_style=False,
            sort_keys=False,
        )
        with open(filename, "w") as file:
            file.write(yaml_data)

    # TODO: toml, xml

    else:
        raise RuntimeError(
            f"store_dict_to_file: No support for PALS file {filename} with extension {extension} yet."
        )
