"""Public, free-standing functions for PALS."""

import os


def inspect_file_extensions(filename: str, sub_level: bool = False):
    """Attempt to strip two levels of file extensions to determine the schema.

    filename examples: fodo.pals.yaml, fodo.pals.json, ...

    Sub-level files, spliced into another file by its `include` entries, use
    the inner extension .subpals per the standard's File Formats section
    (e.g. elements.subpals.yaml); .pals is accepted for them as well.
    """
    file_noext, extension = os.path.splitext(filename)
    file_noext_noext, extension_inner = os.path.splitext(file_noext)

    allowed_inner = (".pals", ".subpals") if sub_level else (".pals",)
    if extension_inner not in allowed_inner:
        expected = " or ".join(f"{inner}.yaml" for inner in allowed_inner)
        raise RuntimeError(
            f"inspect_file_extensions: No support for file {filename} with extension {extension}. "
            f"PALS files must end in {expected} or similar."
        )

    return {
        "file_noext": file_noext,
        "extension": extension,
        "file_noext_noext": file_noext_noext,
        "extension_inner": extension_inner,
    }


def _load_included_file(include_file, base_dir: str, include_chain: tuple):
    """Load the target of one `include` entry, relative to the including file."""
    if not isinstance(include_file, str):
        raise TypeError(
            f"process_includes: an 'include' value must be a file name string, "
            f"but we got {include_file!r}"
        )
    filepath = os.path.join(base_dir, include_file)
    return load_file_to_dict(filepath, sub_level=True, _include_chain=include_chain)


def process_includes(data, base_dir: str, include_chain: tuple = ()):
    """Recursively resolve `include` entries in the data structure.

    Per the standard, included file data is included verbatim at the current
    level of nesting: an `include` key in a mapping splices the included
    mapping's entries into it (entries local to the mapping win), and a list
    item holding only an `include` key splices the included sequence into the
    list. Include file names are resolved relative to the including file.

    Args:
        data: The parsed data structure to resolve
        base_dir: Directory of the file the data came from
        include_chain: Files on the include path so far, for cycle detection

    Returns:
        The data structure with all includes resolved
    """
    if isinstance(data, dict):
        if "include" in data:
            included_data = _load_included_file(
                data["include"], base_dir, include_chain
            )
            if not isinstance(included_data, dict):
                raise TypeError(
                    f"process_includes: file {data['include']!r} is included at a "
                    f"mapping level and must hold a mapping, "
                    f"but we got {type(included_data).__name__}"
                )
            local_data = {
                key: process_includes(value, base_dir, include_chain)
                for key, value in data.items()
                if key != "include"
            }
            # Entries local to the including mapping win over included ones.
            return {**included_data, **local_data}

        return {
            key: process_includes(value, base_dir, include_chain)
            for key, value in data.items()
        }

    elif isinstance(data, list):
        new_list = []
        for item in data:
            # A list item holding only an include splices in the included file
            if isinstance(item, dict) and set(item) == {"include"}:
                included_data = _load_included_file(
                    item["include"], base_dir, include_chain
                )
                if isinstance(included_data, list):
                    new_list.extend(included_data)
                elif isinstance(included_data, dict):
                    new_list.append(included_data)
                else:
                    raise TypeError(
                        f"process_includes: file {item['include']!r} is included at a "
                        f"sequence level and must hold a sequence or mapping, "
                        f"but we got {type(included_data).__name__}"
                    )
            else:
                new_list.append(process_includes(item, base_dir, include_chain))
        return new_list

    else:
        return data


def load_file_to_dict(
    filename: str, sub_level: bool = False, _include_chain: tuple = ()
) -> dict:
    # Guard against include cycles: a file including itself through any chain.
    # realpath canonicalizes symlinks so a cycle cannot hide behind one.
    filepath = os.path.realpath(filename)
    if filepath in _include_chain:
        chain = " -> ".join(_include_chain + (filepath,))
        raise RuntimeError(f"load_file_to_dict: circular include: {chain}")

    # Attempt to strip two levels of file extensions to determine the schema.
    #   Examples: fodo.pals.yaml, fodo.pals.json, ...
    file_noext, extension, file_noext_noext, extension_inner = inspect_file_extensions(
        filename, sub_level=sub_level
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

    # Resolve include entries, tracking this file for cycle detection. In a
    # full document, include statements must be within the PALS root node;
    # information outside of it is outside the standard and is not touched.
    base_dir = os.path.dirname(filename)
    include_chain = _include_chain + (filepath,)
    if isinstance(pals_data, dict) and "PALS" in pals_data:
        pals_data = dict(pals_data)
        pals_data["PALS"] = process_includes(pals_data["PALS"], base_dir, include_chain)
    else:
        pals_data = process_includes(pals_data, base_dir, include_chain)

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
