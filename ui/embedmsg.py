import discord

class embedmsg():
    def __init__(self):
        None

    def createEmbed(self, content, modelName):
        self.content = content
        embedObj = discord.Embed()
        embedObj.add_field(name="prompt", value=self.content["prompt"], inline = False)
        embedObj.add_field(name="negative prompt", value=self.content["negative_prompt"], inline = False)
        embedObj.add_field(name="size", value=str(self.content["height"])+"x"+str(self.content["width"]))
        embedObj.add_field(name="steps", value=self.content["steps"], inline = True)
        embedObj.add_field(name="CFG", value=self.content["cfg_scale"], inline = True)
        embedObj.add_field(name="Sampler", value=self.content["sampler_name"], inline = True)
        embedObj.add_field(name="model", value=modelName, inline = True)
        return embedObj