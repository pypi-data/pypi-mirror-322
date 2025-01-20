"Common code"

# pylint: skip-file


import json
import logging
import os
import re

import yaml

log = logging.getLogger(__name__)


# Setup YAML object
# yaml = ruamel.yaml.YAML()
# yaml.version = (1, 1)
# yaml.default_flow_style = False
# # yaml.indent(mapping=3, sequence=2, offset=0)
# yaml.allow_duplicate_keys = True
# yaml.explicit_start = True


# pylint: disable=redefined-builtin
def truncate(data, max=72, txt=" ..."):
    "Truncate a text to max lenght and replace by txt"
    data = str(data)
    if max < 0:
        return data
    if len(data) > max:
        return data[: max + len(txt)] + txt
    return data


# TODO: Add tests on this one
def to_domain(string, sep=".", alt="-"):
    "Transform any string to valid domain name"

    domain = string.split(sep)
    result = []
    for part in domain:
        part = re.sub("[^a-zA-Z0-9]", alt, part)
        part.strip(alt)
        result.append(part)

    return ".".join(result)


# TODO: Add tests on this one
def first(array):
    "Return the first element of a list or None"
    # return next(iter(array))
    array = list(array) or []
    result = None
    if len(array) > 0:
        result = array[0]
    return result


# TODO: add tests
def from_yaml(string):
    "Transform YAML string to python dict"
    return yaml.load(string)


# TODO: add tests
def to_yaml(obj, headers=False):
    "Transform obj to YAML"
    options = {}
    string_stream = StringIO()

    if isinstance(obj, str):
        obj = json.loads(obj)

    yaml.dump(obj, string_stream, **options)
    output_str = string_stream.getvalue()
    string_stream.close()
    if not headers:
        output_str = output_str.split("\n", 2)[2]
    return output_str


# TODO: add tests
def to_json(obj, nice=True):
    "Transform JSON string to python dict"
    if nice:
        return json.dumps(obj, indent=2)
    return json.dumps(obj)


# TODO: add tests
def from_json(string):
    "Transform JSON string to python dict"
    return json.loads(string)


# TODO: add tests
def to_dict(obj):
    """Transform JSON obj/string to python dict

    Useful to transofmr nested dicts as well"""
    if not isinstance(obj, str):
        obj = json.dumps(obj)
    return json.loads(obj)


def duplicates(_list):
    """Check if given list contains duplicates"""
    known = set()
    dup = set()
    for item in _list:
        if item in known:
            dup.add(item)
        else:
            known.add(item)

    if len(dup) > 0:
        return list(dup)
    return []


def read_file(file):
    "Read file content"
    with open(file, encoding="utf-8") as _file:
        return "".join(_file.readlines())


def write_file(file, content):
    "Write content to file"

    file_folder = os.path.dirname(file)
    if not os.path.exists(file_folder):
        os.makedirs(file_folder)

    with open(file, "w", encoding="utf-8") as _file:
        _file.write(content)


def flatten(array):
    "Flatten any arrays nested arrays"
    if array == []:
        return array
    if isinstance(array[0], list):
        return flatten(array[0]) + flatten(array[1:])
    return array[:1] + flatten(array[1:])


def list_parent_dirs(path):
    """
    Return a list of the parents paths
    path treated as strings, must be absolute path
    """
    result = [path]
    val = path
    while val and val != os.sep:
        val = os.path.split(val)[0]
        result.append(val)
    return result


def find_file_up(names, paths):
    """
    Find every files names in names list in
    every listed paths
    """
    assert isinstance(names, list), f"Names must be array, not: {type(names)}"
    assert isinstance(paths, list), f"Paths must be array, not: {type(names)}"

    result = []
    for path in paths:
        for name in names:
            file_path = os.path.join(path, name)
            if os.access(file_path, os.R_OK):
                result.append(file_path)

    return result


def filter_existing_files(root_path, candidates):
    """Return only existing files"""
    result = [
        os.path.join(root_path, cand)
        for cand in candidates
        if os.path.isfile(os.path.join(root_path, cand))
    ]
    return list(set(result))


def ensure_dir_exists(path):
    """Ensure directories exist for a given path"""
    if not os.path.isdir(path):
        log.info(f"Create directory: {path}")
        os.makedirs(path)
        return True
    return False


def ensure_parent_dir_exists(path):
    """Ensure parent directories exist for a given path"""
    parent = os.path.dirname(os.path.normpath(path))
    return ensure_dir_exists(parent)
