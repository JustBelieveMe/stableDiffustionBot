from ui.EmbedButton import T2iPaintEmbedButton
from ui.modalBase import ModalBase
import discord

class T2i_ui():
    def __init__(self, sdConnecter):
        self.sdConnecter = sdConnecter

    def createDetailpaintui(self, custom_id=None):
        self.detailpaint_ui = Detailt2ipaint_ui(self.sdConnecter)
        return self.detailpaint_ui

    def createEasypaintui(self):
        self.easypaint_ui = Easyt2ipaint_ui(self.sdConnecter)
        return self.easypaint_ui

class Detailt2ipaint_ui(ModalBase, title='Detail T2T Paint'):
    def __init__(self, sdConnecter, setDefault=None):
        super().__init__(sdConnecter, setDefault)
    
    def setDefault(self, fields):
        self.prompt.default = fields[0].value
        self.negative_prompt.default = fields[1].value
        self.size.default = fields[2].value
        self.CFG.default = fields[4].value
        self.sampler.default = fields[5].value
        
    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer(thinking=True)
        self.paint_embedbutton = T2iPaintEmbedButton(self.sdConnecter, interaction.user.id, Detailt2ipaint_ui)
        if self.paraCheck():
            detailJson = {"prompt": self.prompt.value, "negative_prompt":self.negative_prompt.value, "width":self.width, "height":self.height, "sampler":self.sampler.value, "CFG":self.CFG}
            images_ioObj = await self.sdConnecter.detailt2iPaint(detailJson)
            self.embedOBJ = self.embed.createt2iEmbed(self.sdConnecter.gett2iPayload(), self.sdConnecter.getCurrModelName(), interaction.user.name)
            self.imageList = list()
            for image in images_ioObj:
                self.imageList.append(discord.File(image, filename='image.png'))
            await interaction.followup.send(embed=self.embedOBJ, files=self.imageList, view=self.paint_embedbutton)
        else:
            await interaction.followup.send(f'指揮官，你的參數不符合格式！', ephemeral=True)
        
class Easyt2ipaint_ui(ModalBase, title='Easy T2T Paint'):

    def __init__(self, sdConnecter, setDefault=None):
        super().__init__(sdConnecter, setDefault)
        self.remove_item(self.children[1])
        self.remove_item(self.children[1])
        self.remove_item(self.children[1])
        self.remove_item(self.children[1])
    
    def setDefault(self, fields):
        self.prompt.default = fields[0].value

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer(thinking=True) # defer the interaction time
        self.paint_embedbutton = T2iPaintEmbedButton(self.sdConnecter, interaction.user.id, Easyt2ipaint_ui)
        images_ioObj = await self.sdConnecter.easyt2iPaint(self.prompt.value) # pass to sd, await the image return
        self.embedOBJ = self.embed.createt2iEmbed(self.sdConnecter.gett2iPayload(), self.sdConnecter.getCurrModelName(), interaction.user.name, easy=True)
        # handling each image as discord file and form a list
        images = list()
        for image in images_ioObj:
            images.append(discord.File(image, 'image.png'))
        await interaction.followup.send(embed=self.embedOBJ, files=images, view=self.paint_embedbutton)