import json
import os
import sys

from api.modloader import Loader
from pyrogram import Client

config_path = os.path.join(sys.path[0], "config.json")

if not os.path.exists(config_path):
    api_id = input("Enter api_id(from https://my.telegram.org/apps): ")
    api_hash = input("Enter api_hash(from https://my.telegram.org/apps): ")

    with open(config_path, "w") as file:
        json.dump({
            "api_id": api_id,
            "api_hash": api_hash
        }, file, indent=2)
else:
    with open(config_path, "r") as file:
        data = json.load(file)

        api_id = data["api_id"]
        api_hash = data["api_hash"]

app = Client("osp54", api_id, api_hash)

if __name__ == '__main__':
    mods = Loader(app)
    mods.load_modules()
    mods.register_commands()
    mods.register_events()
    mods.send_ready()
    app.run()
