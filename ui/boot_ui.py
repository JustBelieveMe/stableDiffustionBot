import discord

class Bootstrap(discord.ui.View):
    def __init__(self, manageClass, paintClass, modalID, modal, timeout=300):
        super().__init__(timeout=timeout)
        self.modalID = modalID
        self.paintClass = paintClass
        self.modal = modal
        self.manageClass = manageClass

    @discord.ui.button(label='重新使用', style=discord.ButtonStyle.green)
    async def bootstrap(self, interaction, button):
        await interaction.response.send_modal(self.modal(self.paintClass, custom_id=self.modalID))