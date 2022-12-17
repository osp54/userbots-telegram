from pyrogram import Client
from pyrogram.types.messages_and_media import Message

from api import Module
from api.util import command


class helpMod(Module):
    """Provides this help command"""
    info = {"name": "Help"}

    @command("help", "Command list", ["!", "/"])
    async def help(self, client: Client, message: Message):
        reply = ""
        for cmd in self.modules.commands:
            _cmd = cmd['cmd']
            reply += f"**`{_cmd['prefixes']}{_cmd['name']}`** - {_cmd['desc']}" \
                     f" (From {cmd['module'].info['name']} module)\n "
        await message.edit(reply)
