from discord import ui
from ui.embedmsg import Embedmsg
import abc
import discord


class ModalBase(ui.Modal, abc.ABC):
    prompt = ui.TextInput(label='prompt(正面提詞)', style=discord.TextStyle.paragraph)
    negative_prompt = ui.TextInput(label="negative prompt(負面提詞)", style=discord.TextStyle.paragraph, default="nsfw, lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts,signature, watermark, username, blurry")
    size = ui.TextInput(label="image size(圖像大小 widthxheight，最大為1024x1024)", style=discord.TextStyle.short, placeholder="512x512", default="512x512")
    sampler = ui.TextInput(label="sampler(取樣器)", style=discord.TextStyle.short, placeholder="Euler, Euler a ....", default="DPM++ SDE Karras")
    CFG = ui.TextInput(label="CFG(提示詞相關性，越高則模型自由度越低(1~30)。)",style=discord.TextStyle.short, placeholder="1-30", default="7", max_length=2)

    def __init__(self, sdConnecter, setDefault=None):
        super().__init__()
        self.sdConnecter = sdConnecter
        self.samplerOption = self.sdConnecter.getSampler()
        self.embed = Embedmsg()
        if setDefault is not None:
            self.setDefault(setDefault)

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

    @abc.abstractmethod
    def setDefault(self):
        raise NotImplemented
    
