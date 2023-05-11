import discord
from discord import app_commands

class botClient(discord.Client):
    def __init__(self, intents):
        super().__init__(intents = intents)
        self.synced = False
        self.tree = app_commands.CommandTree(self)

    def getTree(self):
        return self.tree

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await self.tree.sync()
            self.synced = True
        print(f'Discord bot activated as {self.user}.')