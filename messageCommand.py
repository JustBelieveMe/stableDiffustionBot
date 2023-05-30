from ui.EmbedButton import I2iPaintEmbedButton
from ui.i2i_ui import Detaili2ipaint_ui, Easyi2ipaint_ui
from ui.embedmsg import I2IEmbedmsg
import discord


class MessageCommand():
    def __init__(self, sdConnecter):
        self.commandDict = dict()
        self.commandDictInit()
        self.sdConnecter = sdConnecter
        # self.i2i_ui = I2i_ui(self.sdConnecter)

    def commandDictInit(self):
        self.commandDict["/detaili2i"] = self.detaili2iPaint
        self.commandDict["/easyi2i"] = self.easyi2iPaint

    def checkCommand(self, command):
        if command in self.getCommandDictKeys():
            return True
        else:
            return False

    def getCommandDictKeys(self):
        return self.commandDict.keys()
    
    async def performCommand(self, message):
        await self.commandDict[message.content](message)

    async def easyi2iPaint(self, message):
        if message.attachments:
            image = self.sdConnecter.getImageFromUrl(message.attachments[0].url)
            imageInfo = self.sdConnecter.checkImage(image)
            if imageInfo[0] == 0:
                embedMsg = I2IEmbedmsg(message.author.name, "easy i2i", message.attachments[0].url)
                await message.channel.send(embed=embedMsg,
                                           view=I2iPaintEmbedButton(self.sdConnecter, 
                                                                    message.author.id,
                                                                    message.attachments[0].url,
                                                                    imageInfo,
                                                                    Easyi2ipaint_ui))
                await message.delete()
            elif imageInfo[0] == 1:
                await message.reply(f"指揮官，你的照片太大張了({imageInfo[1]}x{imageInfo[2]})，請在1024x1024以下。")
            elif imageInfo[0] == 2:
                await message.reply(f"指揮官，你給我的東西是什麼啊???")

    async def detaili2iPaint(self, message):
        if message.attachments:
            image = self.sdConnecter.getImageFromUrl(message.attachments[0].url)
            imageInfo = self.sdConnecter.checkImage(image)
            if imageInfo[0] == 0:
                embedMsg = I2IEmbedmsg(message.author.name, "detail i2i", message.attachments[0].url)
                await message.channel.send(embed=embedMsg,
                                           view=I2iPaintEmbedButton(self.sdConnecter, 
                                                                    message.author.id,
                                                                    message.attachments[0].url,
                                                                    imageInfo,
                                                                    Detaili2ipaint_ui))
                await message.delete()
            elif imageInfo[0] == 1:
                await message.reply(f"指揮官，你的照片太大張了({imageInfo[1]}x{imageInfo[2]})，請在1024x1024以下。")
            elif imageInfo[0] == 2:
                await message.reply(f"指揮官，你給我的東西是什麼啊???")
        else:
            await message.reply("指揮官，你沒有附上任何圖片。")