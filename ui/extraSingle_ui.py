from discord import ui
from ui.embedmsg import Embedmsg
from ui.EmbedButton import ExtraDeleteEmbedButton
import discord

class Extra_ui(ui.Modal, title="extra single image"):
    size = ui.TextInput(label='upscaling_resize(放大尺寸)', style=discord.TextStyle.short, default="2")
    upscaler_1 = ui.TextInput(label="upscaler_1(上取樣器1)", style=discord.TextStyle.paragraph, default="R-ESRGAN 4x+")
    upscaler_2 = ui.TextInput(label="upscaler_2(上取樣器2)", style=discord.TextStyle.paragraph,  default="None")
    
    def __init__(self, sdConnecter, url):
        super().__init__()
        self.sdConnecter = sdConnecter
        self.image_url = url
        self.upscaler = self.sdConnecter.getUpscaler()
    
    def paraCheck(self):
        #sampler check
        self.size = int(self.size.value)
        if self.upscaler_1.value not in self.upscaler or self.upscaler_2.value not in self.upscaler:
            return False
        if self.size < 0 or self.size > 8:
            return False
        return True

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer(thinking=True)
        self.extrad_delete_embed_button = ExtraDeleteEmbedButton(interaction.user.id)
        if self.paraCheck():
            self.detailJson ={"upscaling_resize": self.size,
                            "upscaler_1":self.upscaler_1.value,
                            "upscaler_2":self.upscaler_2.value}
            images_ioObj = await self.sdConnecter.extra_single(self.detailJson, self.image_url)
            await interaction.followup.send(file=discord.File(images_ioObj, filename='image.png'), view=self.extrad_delete_embed_button)
        else:
            await interaction.followup.send(f'指揮官，你的參數不符合格式！', ephemeral=True)
