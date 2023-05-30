import discord
from discord import app_commands

class botClient(discord.Client):
    def __init__(self, modelstatus, version):
        self.modelstatus = modelstatus
        intents = discord.Intents.default()
        intents.typing = False
        intents.presences = False
        intents.messages = True
        intents.message_content = True
        intents.members = True
        super().__init__(intents = intents)
        self.synced = False
        self.tree = app_commands.CommandTree(self)
        self.version = version

    def getTree(self):
        return self.tree

    def getVersion(self):
        return self.version
    
    async def changeDisplayModel(self, modelName):
        await self.change_presence(activity=discord.Game(f"機器人版本{self.getVersion()}\n正在運作: {modelName}"))

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await self.tree.sync()
            self.synced = True
        await self.changeDisplayModel(self.modelstatus)
        print(f'Discord bot activated as {self.user}.')

