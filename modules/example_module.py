from pyrogram import Client, handlers
from pyrogram.types.messages_and_media import Message

from api import Module
from api.util import command, on_event


class exampleMod(Module):
    """Example module"""

    @command("ping", "Check the module is working", "!")
    async def ping(self, client, message: Message):
        await message.edit("Pong!")

    @on_event(handlers.MessageHandler)
    async def on_message(self, client, message):
        pass
        # Working with the message

    def on_ready(self):
        pass
        # Here you can register commands without decorators via self.client.add_handler()
