import discord

class Embedmsg():
    def __init__(self):
        None

    def createt2iEmbed(self, content, modelName, author_name, easy=False):
        self.content = content
        embedObj = discord.Embed()
        if len(self.content["prompt"]) > 1024:
            embedObj.add_field(name="prompt", value=self.content["prompt"][0:1000], inline = False)
        else:
            embedObj.add_field(name="prompt", value=self.content["prompt"], inline = False)
        if not easy:
            if len(self.content["negative_prompt"]) > 1024:
                embedObj.add_field(name="negative prompt", value=self.content["negative_prompt"][0:1000], inline = False)
            else:
                embedObj.add_field(name="negative prompt", value=self.content["negative_prompt"], inline = False)
            embedObj.add_field(name="size", value=str(self.content["width"])+"x"+str(self.content["height"]))
            embedObj.add_field(name="steps", value=self.content["steps"], inline = True)
            embedObj.add_field(name="CFG", value=self.content["cfg_scale"], inline = True)
            embedObj.add_field(name="Sampler", value=self.content["sampler_name"], inline = True)
        embedObj.add_field(name="model", value=modelName, inline = True)
        embedObj.add_field(name="Image author", value = author_name, inline = False)
        return embedObj
    
    def createi2iEmbed(self, content, image_url, modelName, author_name, easy=False):
        #0: prompt, (1:ng_prompt, 2:cfg, 3:sampler), 4:size, 5:denoisy, 6:url, 7:model, 8, author
        self.content = content
        embedObj = discord.Embed()
        if len(self.content["prompt"]) > 1024:
            embedObj.add_field(name="prompt", value=self.content["prompt"][0:1000], inline = False) 
        else:
            embedObj.add_field(name="prompt", value=self.content["prompt"], inline = False)
        if not easy:
            if len(self.content["negative_prompt"]) > 1024:
                embedObj.add_field(name="negative prompt", value=self.content["negative_prompt"][0:1000], inline = False)
            else:
                embedObj.add_field(name="negative prompt", value=self.content["negative_prompt"], inline = False)
            embedObj.add_field(name="CFG", value=self.content["cfg_scale"], inline = True)
            embedObj.add_field(name="Sampler", value=self.content["sampler_name"], inline = True)
        embedObj.add_field(name="size", value=str(self.content["width"])+"x"+str(self.content["height"]))
        embedObj.add_field(name="denoisy strength", value=self.content["denoising_strength"], inline=True)
        embedObj.add_field(name="original image url", value=image_url, inline=True)
        embedObj.add_field(name="model", value=modelName, inline = True)
        embedObj.add_field(name="Image author", value = author_name, inline = False)
        return embedObj
    
class I2IEmbedmsg(discord.Embed):
    def __init__(self, author_name, mode, image_url):
        super().__init__()
        self.add_field(name="Image uploader", value = author_name, inline=True)
        self.add_field(name="i2i mode", value = mode, inline=True)
        self.set_image(url=image_url)

class ExtraEmbedmsg(discord.Embed):
    def __init__(self, author_name, mode, image_url):
        super().__init__()
        self.add_field(name="Image uploader", value = author_name, inline=True)
        self.add_field(name="extra mode", value = mode, inline=True)
        self.set_image(url=image_url)

class HelpEmbedMessage(discord.Embed):
    def __init__(self, helpMessage):
        super().__init__()
        self.helpMessage = helpMessage
        self.title=self.helpMessage["title"]+self.helpMessage["version"]
        self.add_field(name="更新日期", value = self.helpMessage["upgradeDate"], inline=True)
        self.add_field(name='最新公告', value=self.helpMessage['announcement'], inline=False)
        self.add_field(name='一般說明', value=self.helpMessage['description'], inline=False)
        self.add_field(name='協助指令', value=self.helpMessage['help'], inline=False)
        self.add_field(name='詞生圖指令', value=self.helpMessage["Text2Img"], inline=False)
        self.add_field(name='圖生圖指令', value=self.helpMessage["Img2Img"], inline=False)
        self.add_field(name="取樣器(Sampler)的選項",value=self.helpMessage["Sampler"], inline=False)