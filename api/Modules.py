import os
import sys
import importlib.util
from pyrogram import Client
from types import ModuleType


def command(name, prefix, aliases):
    def decorator(function):
        setattr(function, "command", {name: {
            "prefix": prefix,
            "aliases": aliases,
            "fun": function
        }})
        return function

    return decorator


class Module():
    info = {"name": "Unknown"}
    commands = []

    def __init__(self, client: Client):
        self.client = client

    def on_ready(self):
        """Will be called when the client is ready"""


class Modules():
    def __init__(self, client: Client):
        self.client = client
        self.modules = []
        self.modules_dir = os.path.join(sys.path[0], "modules")

    def load_modules(self):
        for file in os.listdir(self.modules_dir):
            if file.endswith(".py"):
                module = self.load_file(file)
                for k, v in vars(module).items():
                    if k.endswith("Mod") and issubclass(v, Module):
                        mod = v()
                        self.modules.append(mod)
                        self.load_module(mod)

    @staticmethod
    def load_module(module: Module):
        for mod_v in dir(module):
            attr = getattr(module, mod_v)
            if callable(attr) and hasattr(attr, "command"):
                module.commands.append(attr.command)

    @staticmethod
    def load_file(file) -> ModuleType:
        file_path = os.path.join(self.modules_dir, file)
        module_name = f"{__package__}.modules.{file[:-3]}"
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return load_module
