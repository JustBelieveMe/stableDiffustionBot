import discord

class T2iPaintEmbedButton(discord.ui.View):
    def __init__(self, sdConnecter, authorID, sentModal):
        super().__init__(timeout=None)
        self.sdConnecter = sdConnecter
        self.authorID = authorID
        self.sentModal = sentModal

    @discord.ui.button(label='重新使用', style=discord.ButtonStyle.green)
    async def repaint(self, interaction, button):
        await interaction.response.send_modal(self.sentModal(self.sdConnecter, setDefault=interaction.message.embeds[0].fields))

    @discord.ui.button(label='移除圖片', style=discord.ButtonStyle.red)
    async def remove(self, interaction, button):
        if interaction.user.id == self.authorID:
            await interaction.message.delete()
        else:
            await interaction.response.send_message("指揮官，你不是原始作者，不能刪除。", ephemeral=True)

class I2iPaintEmbedButton(discord.ui.View):
    def __init__(self, sdConnecter, authorID, url, image_info, sentModal):
        super().__init__(timeout=None)
        self.authorID = authorID
        self.sentModal = sentModal
        self.image_info = image_info
        self.image_url = url
        self.sdConnecter = sdConnecter

    @discord.ui.button(label='開始使用', style=discord.ButtonStyle.green)
    async def repaint(self, interaction, button):
        await interaction.response.send_modal(self.sentModal(self.sdConnecter, self.image_url, self.image_info[1], self.image_info[2]))

    @discord.ui.button(label='移除圖片', style=discord.ButtonStyle.red)
    async def remove(self, interaction, button):
        if interaction.user.id == self.authorID:
            await interaction.message.delete()
        else:
            await interaction.response.send_message("指揮官，你不是原始作者，不能刪除。", ephemeral=True)


class I2iRepaintEmbedButton(discord.ui.View):
    def __init__(self,sdConnecter, authorID, sentModal):
        super().__init__(timeout=None)
        self.sdConnecter = sdConnecter
        self.authorID = authorID
        self.sentModal = sentModal

    @discord.ui.button(label='重新使用', style=discord.ButtonStyle.green)
    async def repaint(self, interaction, button):
        await interaction.response.send_modal(self.sentModal(self.sdConnecter,None, None, None, setDefault=interaction.message.embeds[0].fields))

    @discord.ui.button(label='移除圖片', style=discord.ButtonStyle.red)
    async def remove(self, interaction, button):
        if interaction.user.id == self.authorID:
            await interaction.message.delete()
        else:
            await interaction.response.send_message("指揮官，你不是原始作者，不能刪除。", ephemeral=True)