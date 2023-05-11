from discord import ui
import discord

class AddUser(ui.Modal, title='add new auth user'):
    userID = ui.TextInput(label='使用者ID', style=discord.TextStyle.paragraph)

    def __init__(self, userManagement, botGetIdFunc):
        super().__init__()
        self.userManagement = userManagement
        self.getUserFunc = botGetIdFunc
        
    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer(thinking=True)
        self.newUserName = self.getUserFunc(int(self.userID.value))
        if self.newUserName is None:
            await interaction.followup.send(f'指揮官，您給的ID可能是錯的！')
        else:
            if self.userManagement.addUser(int(self.userID.value)):
                await interaction.followup.send(f'指揮官，使用者 {self.newUserName} 已經註冊！')
            else:
                await interaction.followup.send(f'指揮官，使用者 {self.newUserName} 本來就在列表內！')

class DeleteUser(ui.Modal, title='delete auth user'):
    userID = ui.TextInput(label='使用者ID', style=discord.TextStyle.paragraph)

    def __init__(self, userManagement, botGetIdFunc):
        super().__init__()
        self.userManagement = userManagement
        self.getUserFunc = botGetIdFunc

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer(thinking=True)
        self.oldUserName = self.getUserFunc(int(self.userID.value))
        if self.newUserName is None:
            await interaction.followup.send(f'指揮官，您給的ID可能是錯的！')
        else:
            if self.userManagement.deleteUser(int(self.userID.value)):
                await interaction.followup.send(f'指揮官，使用者{self.oldUserName}已經移除！')
            else:
                await interaction.followup.send(f'指揮官，使用者{self.oldUserName}本來就不在列表內！')
        