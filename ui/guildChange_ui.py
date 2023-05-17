# dep, not in use

from discord import ui
import discord

class AddGuild(ui.Modal, title='add new auth guild'):
    guildID = ui.TextInput(label='伺服器ID', style=discord.TextStyle.paragraph)

    def __init__(self, guildManagement, botGetIdFunc):
        super().__init__()
        self.guildManagement = guildManagement
        self.getUserFunc = botGetIdFunc
        
    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer(thinking=True)
        self.newUserName = self.getUserFunc(int(self.userID.value))
        if self.newUserName is None:
            await interaction.followup.send(f'指揮官，您給的ID可能是錯的！')
        else:
            if self.guildManagement.addUser(int(self.userID.value)):
                await interaction.followup.send(f'指揮官，使用者 {self.newUserName} 已經註冊！')
            else:
                await interaction.followup.send(f'指揮官，使用者 {self.newUserName} 本來就在列表內！')

class DeleteGuild(ui.Modal, title='delete auth guild'):
    guildID = ui.TextInput(label='伺服器ID', style=discord.TextStyle.paragraph)

    def __init__(self, guildManagement, botGetIdFunc):
        super().__init__()
        self.guildManagement = guildManagement
        self.getUserFunc = botGetIdFunc

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer(thinking=True)
        self.oldUserName = self.getUserFunc(int(self.userID.value))
        if self.newUserName is None:
            await interaction.followup.send(f'指揮官，您給的ID可能是錯的！')
        else:
            if self.guildManagement.deleteUser(int(self.userID.value)):
                await interaction.followup.send(f'指揮官，使用者{self.oldUserName}已經移除！')
            else:
                await interaction.followup.send(f'指揮官，使用者{self.oldUserName}本來就不在列表內！')
        