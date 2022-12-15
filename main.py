import json
import os
import sys
import importlib.util

from api.Modules import Modules
from pyrogram import Client, filters
from pyrogram.types import Message

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


@app.on_message(filters.command("ping", "!"))
async def ping(client, message: Message):
    await message.edit("Pong!")


if __name__ == '__main__':
    mods = Modules()
    mods.load_modules()

    for mod in mods.modules:
        for cmd in mod.commands:

    app.run()
