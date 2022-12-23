import os
import sys
import importlib.util
from functools import partial
from types import ModuleType

from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler


class Module:
    info = {"name": "Unknown"}
    client: Client

    def on_ready(self):
        """Called when the modules are loaded"""

    modules = None


class Loader:
    modules = []
    commands = []
    events = []
    handlers = []

    def __init__(self, client: Client):
        self.client = client
        self.modules_dir = os.path.join(sys.path[0], "modules")

    def load_modules(self):
        for file in os.listdir(self.modules_dir):
            if file.endswith(".py"):
                module = self.load_file(file)
                for k, v in vars(module).items():
                    if k.endswith("Mod") and issubclass(v, Module):
                        mod = v()
                        self.load_module(mod)

    def load_module(self, module: Module):
        self.modules.append(module)
        for mod_v in dir(module):
            attr = getattr(module, mod_v)
            if callable(attr):
                if hasattr(attr, "command"):
                    self.commands.append({
                        "cmd": attr.command,
                        "module": module
                    })
                if hasattr(attr, "event"):
                    self.events.append({
                        "event": attr.event,
                        "module": module
                    })

    def load_file(self, file) -> ModuleType:
        file_path = os.path.join(self.modules_dir, file)
        module_name = f"{__package__}.modules.{file[:-3]}"
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def register_commands(self):
        for cmd in self.commands:
            handler = self.client.add_handler(MessageHandler(partial(cmd["cmd"]["function"], cmd["module"])
                                                             , filters.command(cmd["cmd"]["name"],
                                                                               cmd["cmd"]["prefixes"])),
                                              0)
            self.handlers.append({
                "handler": handler,
                "module": cmd["module"],
                "function": cmd["cmd"]["function"]
            })

    def register_events(self):
        for event in self.events:
            handler = self.client.add_handler(
                event["event"]["event"](partial(event["event"]["function"], event["module"]), event["event"]["filter"]))
            self.handlers.append({
                "handler": handler,
                "module": event["module"],
                "function": event["event"]["function"]
            })

    def send_ready(self):
        for mod in self.modules:  # type: Module
            mod.modules = self
            mod.client = self.client

            mod.on_ready()
