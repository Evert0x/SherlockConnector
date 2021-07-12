import importlib
import os
import json
import pkgutil

def enumerate_abi(dirpath):
    if os.path.isfile(dirpath):
        dirpath = os.path.dirname(dirpath)

    ret = {}

    for filename in os.listdir(dirpath):
        if not filename.endswith('.json'):
            continue

        with open(os.path.join(dirpath, filename)) as f:
            data = json.load(f)

        name = filename[:len(filename) - 5]
        ret[name] = data

    return ret

def enumerate_plugins(dirpath, module_prefix, class_):
    if os.path.isfile(dirpath):
        dirpath = os.path.dirname(dirpath)

    for _, module_name, _ in pkgutil.iter_modules([dirpath], module_prefix+"."):
        try:
            importlib.import_module(module_name)
        except ImportError as e:
            raise ValueError(
                "Unable to load the plugin at %s: %s." % (module_name, e)
            )

    subclasses = class_.__subclasses__()[:]

    plugins = []
    while subclasses:
        subclass = subclasses.pop(0)
        subclasses.extend(subclass.__subclasses__())

        if not subclass.__module__.startswith(module_prefix):
            continue
        plugins.append(subclass)

    ret = {}
    for plugin in plugins:
        ret[plugin.__name__] = plugin
    return ret