from api.Modules import Module, command


class nysaMod(Module):
    info = {"name": "Unknown"}
    commands = []

    @command("test", "!", ["n", "b"])
    async def nya(self):
        print("test")

