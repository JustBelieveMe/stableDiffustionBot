from discord import ui
from ui.boot_ui import Bootstrap
import discord

class Detailpaint(ui.Modal, title='Detailpaint'):
    prompt = ui.TextInput(label='prompt(正面提詞)', style=discord.TextStyle.paragraph)
    negative_prompt = ui.TextInput(label="negative prompt(負面提詞)", style=discord.TextStyle.paragraph)
    size = ui.TextInput(label="image size(圖像大小 widthxheight，最大為1024x1024)", style=discord.TextStyle.short, placeholder="512x512", default="512x512")
    sampler = ui.TextInput(label="sampler(取樣器)", style=discord.TextStyle.short, placeholder="Euler, Euler a ....", default="DPM++ SDE Karras")
    CFG = ui.TextInput(label="CFG(提示詞相關性，越高則模型自由度越低(1~30)。)",style=discord.TextStyle.short, placeholder="1-30", default="7", max_length=2)

    def __init__(self, paintClass, custom_id=None):
        if custom_id is None:
            super().__init__()
        else:
            super().__init__(custom_id=custom_id)
        self.paintClass = paintClass
        self.detailPaint = self.paintClass.detailPaint
        self.samplerOption = self.paintClass.getSampler()
        # self.boot = Bootstrap(self.paintClass, self.custom_id, self)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer(thinking=True)
        if self.paraCheck():
            detailJson = {"prompt": self.prompt.value, "ng_prompt":self.negative_prompt.value, "width":self.width, "height":self.height, "sampler":self.sampler.value, "CFG":self.CFG}
            images_ioObj =  self.detailPaint(detailJson)
            images = list()
            for image in images_ioObj:
                images.append(discord.File(image, 'image.png'))
            await interaction.followup.send(f'指揮官，這是你要的結果！', files=images)
            # await interaction.followup.send(f'指揮官，這是你要的結果！', files=images, view=self.boot)
        else:
            await interaction.followup.send(f'指揮官，你的參數不符合格式！')
            # await interaction.followup.send(f'指揮官，你的參數不符合格式！', view=self.boot)

    def paraCheck(self):
        #size check
        if "x" in self.size.value:
            self.size = self.size.value.split("x")
        else:
            return False
        try:
            self.width = int(self.size[0])
            self.height = int(self.size[1])
        except ValueError:
            return False
        if self.width > 1024 or self.width < 1 or self.height > 1024 or self.height < 1:
            return False
        
        #sampler check
        if self.sampler.value not in self.samplerOption:
            return False
        
        #CFG check
        try:
            self.CFG = int(self.CFG.value)
        except ValueError:
            return False
        if self.CFG < 1 or self.CFG > 30:
            return False
        
        return True
        
class Easypaint(ui.Modal, title='Easypaint'):
    prompt = ui.TextInput(label='prompt(正面提詞)', style=discord.TextStyle.paragraph)

    def __init__(self, paintClass):
        super().__init__()
        self.paintClass = paintClass

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer(thinking=True)
        images_ioObj =  self.paintClass.easyPaint(self.prompt.value)
        images = list()
        for image in images_ioObj:
            images.append(discord.File(image, 'image.png'))
        await interaction.followup.send(f'指揮官，這是你要的結果！', files=images)