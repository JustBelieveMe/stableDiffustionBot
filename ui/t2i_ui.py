from discord import ui
from ui.embedmsg import embedmsg
import discord

class T2i_ui():
    def __init__(self):
        None
    def createDetailpaintui(self, sdConnecter, custom_id=None):
        self.Detailpaint_ui = Detailpaint_ui(sdConnecter)
        return self.Detailpaint_ui

    def createEasypaintui(self):
        None

class Detailpaint_ui(ui.Modal, title='Detailpaint'):
    prompt = ui.TextInput(label='prompt(正面提詞)', style=discord.TextStyle.paragraph)
    negative_prompt = ui.TextInput(label="negative prompt(負面提詞)", style=discord.TextStyle.paragraph, default="nsfw, lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts,signature, watermark, username, blurry")
    size = ui.TextInput(label="image size(圖像大小 widthxheight，最大為1024x1024)", style=discord.TextStyle.short, placeholder="512x512", default="512x512")
    sampler = ui.TextInput(label="sampler(取樣器)", style=discord.TextStyle.short, placeholder="Euler, Euler a ....", default="DPM++ SDE Karras")
    CFG = ui.TextInput(label="CFG(提示詞相關性，越高則模型自由度越低(1~30)。)",style=discord.TextStyle.short, placeholder="1-30", default="7", max_length=2)

    def __init__(self, sdConnecter, setDefault = None):
        super().__init__()
        self.sdConnecter = sdConnecter
        self.samplerOption = self.sdConnecter.getSampler()
        self.embed = embedmsg()
        if setDefault is not None:
            self.setDefault(setDefault)
    
    def setDefault(self, fields):
        self.prompt.default = fields[0].value
        self.negative_prompt.default = fields[1].value
        self.size.default = fields[2].value
        self.CFG.default = fields[4].value
        self.sampler.default = fields[5].value
        
    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer(thinking=True)
        self.EmbedButton = EmbedButton(self.sdConnecter, interaction.user.id)
        if self.paraCheck():
            detailJson = {"prompt": self.prompt.value, "negative_prompt":self.negative_prompt.value, "width":self.width, "height":self.height, "sampler":self.sampler.value, "CFG":self.CFG}
            images_ioObj = await self.sdConnecter.detailPaint(detailJson)
            self.embedOBJ = self.embed.createEmbed(self.sdConnecter.getPayload(), self.sdConnecter.getCurrModelName(), interaction.user.name)
            self.imageList = list()
            for image in images_ioObj:
                self.imageList.append(discord.File(image, filename='image.png'))
            await interaction.followup.send(embed=self.embedOBJ, files=self.imageList, view=self.EmbedButton, username=interaction.user.name)
            # await interaction.followup.send(f'指揮官，這是你要的結果！', files=images, view=self.boot)
        else:
            await interaction.followup.send(f'指揮官，你的參數不符合格式！', ephemeral=True)
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
        if self.width > 1024 or self.width < 100 or self.height > 1024 or self.height < 100:
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
        
class Easypaint_ui(ui.Modal, title='Easypaint'):
    prompt = ui.TextInput(label='prompt(正面提詞)', style=discord.TextStyle.paragraph)

    def __init__(self, sdConnecter):
        super().__init__()
        self.sdConnecter = sdConnecter

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer(thinking=True) # defer the interaction time
        images_ioObj = await self.sdConnecter.easyPaint(self.prompt.value) # pass to sd, await the image return

        # handling each image as discord file and form a list
        images = list()
        for image in images_ioObj:
            images.append(discord.File(image, 'image.png'))
        await interaction.followup.send(f'指揮官，這是你要的結果！', files=images)

class EmbedButton(discord.ui.View):
    def __init__(self, sdConnecter, authorID):
        super().__init__()
        self.sdConnecter = sdConnecter
        self.authorID = authorID

    @discord.ui.button(label='重新使用', style=discord.ButtonStyle.green)
    async def repaint(self, interaction, button):
        await interaction.response.send_modal(Detailpaint_ui(self.sdConnecter, setDefault=interaction.message.embeds[0].fields))

    @discord.ui.button(label='移除圖片', style=discord.ButtonStyle.red)
    async def remove(self, interaction, button):
        if interaction.user.id == self.authorID:
            await interaction.message.delete()
        else:
            await interaction.response.send_message("指揮官，你不是原始作者，不能刪除。", ephemeral=True)

    async def on_timeout(self):
        None