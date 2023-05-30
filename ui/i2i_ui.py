from discord import ui
from ui.embedmsg import Embedmsg
from ui.EmbedButton import I2iRepaintEmbedButton
from ui.modalBase import ModalBase
import discord

class I2i_ui():
    def __init__(self, sdConnecter):
        self.sdConnecter = sdConnecter
        
    def createi2idetailpaintui(self, url, imageInfo):
        self.detaili2ipaint_ui = Detaili2ipaint_ui(self.sdConnecter, url, imageInfo[1], imageInfo[2])
        return self.detaili2ipaint_ui

    def createi2ieasypaintui(self, url):
        self.easyi2ipaint_ui = Easyi2ipaint_ui(self.sdConnecter)
        return self.easyi2ipaint_ui

class Detaili2ipaint_ui(ModalBase, title="Detail I2I Paint"):
    def __init__(self, sdConnecter, url, width, height, setDefault=None):
        super().__init__(sdConnecter)
        self.remove_item(self.children[2]) #delete size
        self.denoising_strength = ui.TextInput(label="denoising strength(重繪幅度)", style=discord.TextStyle.short, placeholder="0-1", default="0.75")
        self.add_item(self.denoising_strength)
        self.image_url = url
        self.width = width
        self.height = height
        if setDefault is not None:
            self.setDefault(setDefault)
        else:
            self.defaultData = None

    def paraCheck(self):
        #sampler check
        if self.sampler.value not in self.samplerOption:
            return False
        
        #CFG check
        try:
            self.cfg = int(self.CFG.value)
        except ValueError:
            return False
        if self.cfg < 1 or self.cfg > 30:
            return False

        # denoising_strength check
        try:
            self.denoising_strength = float(self.denoising_strength.value)
        except ValueError:
            return False
        if self.denoising_strength > 1 or self.denoising_strength < 0:
            return False
        return True
        
    def setDefault(self, fields):
        self.prompt.default = fields[0].value
        self.negative_prompt.default = fields[1].value
        self.CFG.default = fields[2].value
        self.sampler.default = fields[3].value
        size = fields[4].value.split("x")
        self.width = int(size[0])
        self.height = int(size[1])
        self.denoising_strength.default = fields[5].value
        self.image_url = fields[6].value
        
    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer(thinking=True)
        self.paint_embedbutton = I2iRepaintEmbedButton(self.sdConnecter, 
                                                     interaction.user.id, 
                                                     Detaili2ipaint_ui)
        if self.paraCheck():
            self.detailJson ={"prompt": self.prompt.value,
                            "negative_prompt":self.negative_prompt.value,
                            "width":self.width, "height":self.height,
                            "sampler":self.sampler.value,
                            "CFG":self.cfg,
                            "denoising_strength":self.denoising_strength}
            images_ioObj = await self.sdConnecter.detaili2iPaint(self.detailJson, self.image_url)
            self.embedOBJ = self.embed.createi2iEmbed(self.sdConnecter.geti2iPayload(), self.image_url, self.sdConnecter.getCurrModelName(), interaction.user.name)
            self.imageList = list()
            for image in images_ioObj:
                self.imageList.append(discord.File(image, filename='image.png'))
            await interaction.followup.send(embed=self.embedOBJ, files=self.imageList, view=self.paint_embedbutton)
        else:
            await interaction.followup.send(f'指揮官，你的參數不符合格式！', ephemeral=True)
        

class Easyi2ipaint_ui(Detaili2ipaint_ui, title="Easy I2I Paint"):
    def __init__(self, sdConnecter, url, width, height, setDefault=None):
        super().__init__(sdConnecter, url, width, height, setDefault=setDefault)
        self.remove_item(self.children[1])
        self.remove_item(self.children[2])
        self.remove_item(self.children[1])

    def setDefault(self, fields):
        self.prompt.default = fields[0].value
        size = fields[1].value.split("x")
        self.width = int(size[0])
        self.height = int(size[1])
        self.denoising_strength.default = fields[2].value
        self.image_url = fields[3].value

    def paraCheck(self):
        # denoising_strength check
        try:
            self.denoising_strength = float(self.denoising_strength.value)
        except ValueError:
            return False
        if self.denoising_strength > 1 or self.denoising_strength < 0:
            return False
        return True

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer(thinking=True)
        self.paint_embedbutton = I2iRepaintEmbedButton(self.sdConnecter, 
                                                     interaction.user.id, 
                                                     Easyi2ipaint_ui)
        if self.paraCheck():
            self.detailJson ={"prompt": self.prompt.value,
                            "width":self.width, "height":self.height,
                            "denoising_strength":self.denoising_strength}
            images_ioObj = await self.sdConnecter.easyi2iPaint(self.detailJson, self.image_url)
            self.embedOBJ = self.embed.createi2iEmbed(self.sdConnecter.geti2iPayload(), self.image_url, self.sdConnecter.getCurrModelName(), interaction.user.name, easy=True)
            self.imageList = list()
            for image in images_ioObj:
                self.imageList.append(discord.File(image, filename='image.png'))
            await interaction.followup.send(embed=self.embedOBJ, files=self.imageList, view=self.paint_embedbutton)
        else:
            await interaction.followup.send(f'指揮官，你的參數不符合格式！', ephemeral=True)