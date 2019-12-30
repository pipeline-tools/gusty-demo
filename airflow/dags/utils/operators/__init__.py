import importlib
import pkgutil

import os
import inspect

available_builds = {}

def register_build(build_func):
    frame = inspect.stack()[1]
    filename = frame[0].f_code.co_filename
    operator_name = os.path.splitext(os.path.basename(filename))[0]
    available_builds.update({operator_name:build_func})

def import_submodules(package, recursive=True):
    """
    Import all submodules of a module, recursively, including subpackages
    """
    if isinstance(package, str):
        package = importlib.import_module(package)
    results = {}
    for loader, name, is_pkg in pkgutil.walk_packages(package.__path__):
        full_name = package.__name__ + '.' + name
        results[full_name] = importlib.import_module(full_name)
        if recursive and is_pkg:
            results.update(import_submodules(full_name))
    return results

import_submodules(__name__, recursive=False)
