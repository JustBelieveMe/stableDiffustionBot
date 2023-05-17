import discord
from discord import app_commands

class botClient(discord.Client):
    def __init__(self, modelstatus):
        self.modelstatus = modelstatus
        intents = discord.Intents.default()
        intents.typing = False
        intents.presences = False
        intents.messages = True
        intents.members = True
        super().__init__(intents = intents)
        self.synced = False
        self.tree = app_commands.CommandTree(self)

    def getTree(self):
        return self.tree
    
    async def changeDisplayModel(self, modelName):
        await self.change_presence(activity=discord.Game(f"正在運作: {modelName}"))

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await self.tree.sync()
            self.synced = True
        await self.changeDisplayModel(self.modelstatus)
        print(f'Discord bot activated as {self.user}.')

