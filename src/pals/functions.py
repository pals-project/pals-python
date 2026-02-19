"""Public, free-standing functions for PALS."""

import os


def inspect_file_extensions(filename: str, check_extension: bool = True):
    """Attempt to strip two levels of file extensions to determine the schema.

    filename examples: fodo.pals.yaml, fodo.pals.json, ...
    """
    file_noext, extension = os.path.splitext(filename)
    file_noext_noext, extension_inner = os.path.splitext(file_noext)

    if check_extension and extension_inner != ".pals":
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


def process_includes(data, base_dir: str):
    """Recursively process 'include' directives in the data structure."""
    if isinstance(data, dict):
        # Handle 'include' key in dictionary
        if "include" in data:
            include_file = data["include"]
            # Check if include_file is a string (filename)
            if isinstance(include_file, str):
                filepath = os.path.join(base_dir, include_file)
                # Load included file without strict extension check
                included_data = load_file_to_dict(filepath, check_extension=False)

                # Remove 'include' key
                local_data = data.copy()
                del local_data["include"]

                # Recursively process local data
                local_data = {
                    k: process_includes(v, base_dir) for k, v in local_data.items()
                }

                # Merge logic
                # If included data is a list of single-key dicts (PALS special case), try to merge as dict
                if isinstance(included_data, list):
                    try:
                        merged_included = {}
                        all_dicts = True
                        for item in included_data:
                            if isinstance(item, dict) and len(item) == 1:
                                merged_included.update(item)
                            else:
                                all_dicts = False
                                break
                        if all_dicts:
                            included_data = merged_included
                    except Exception:
                        pass

                if isinstance(included_data, dict):
                    # Merge included data with local data (local overrides included?)
                    # Spec: "Included file data will be included verbatim at the current level of nesting."
                    # Usually specific (local) overrides generic (included).
                    # So we take included, update with local.
                    result = included_data.copy()
                    result.update(local_data)
                    return result
                else:
                    # If included data is not a dict, we can't merge it into a dict.
                    # Unless the dict was JUST the include?
                    if not local_data:
                        return included_data
                    # Fallback: return local data (ignore include) or error?
                    # For now, let's return local_data but maybe warn?
                    # Or maybe return included_data if local_data is empty?
                    return local_data

        # Recurse on values if no include or after processing
        return {k: process_includes(v, base_dir) for k, v in data.items()}

    elif isinstance(data, list):
        new_list = []
        for item in data:
            # Check if item is a dict with ONLY 'include' key
            if isinstance(item, dict) and "include" in item and len(item) == 1:
                include_file = item["include"]
                if isinstance(include_file, str):
                    filepath = os.path.join(base_dir, include_file)
                    included_data = load_file_to_dict(filepath, check_extension=False)

                    if isinstance(included_data, list):
                        new_list.extend(included_data)
                    else:
                        new_list.append(included_data)
                else:
                    new_list.append(process_includes(item, base_dir))
            else:
                new_list.append(process_includes(item, base_dir))
        return new_list

    else:
        return data


def load_file_to_dict(filename: str, check_extension: bool = True) -> dict:
    # Attempt to strip two levels of file extensions to determine the schema.
    #   Examples: fodo.pals.yaml, fodo.pals.json, ...
    file_noext, extension, file_noext_noext, extension_inner = inspect_file_extensions(
        filename, check_extension=check_extension
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

    # Process includes
    pals_data = process_includes(pals_data, base_dir=os.path.dirname(filename))

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
