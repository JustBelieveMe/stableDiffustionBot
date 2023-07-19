#  https://discordapp.com/oauth2/authorize?&client_id=772092610104918017&scope=bot&permissions=8

import discord
import json
from botClient import botClient
from ui.t2i_ui import T2i_ui
from ui.sdselect_ui import select_ui
from ui.embedmsg import HelpEmbedMessage
from sdConnecter import SDConnecter
from authManagement import authManagement
from messageCommand import MessageCommand

with open("./variables.json", "r", encoding="utf-8") as variableFile:
    variables = json.load(variableFile)

with open("./jsonfile/helpMessage.json", "r", encoding='utf-8') as helpMsgFile:
    helpMessage = json.load(helpMsgFile)

sdConnecter = SDConnecter()
authManagement = authManagement()
client = botClient(sdConnecter.getCurrModelName(), helpMessage["version"])
tree = client.getTree()
t2i_ui = T2i_ui(sdConnecter)
messageCommand = MessageCommand(sdConnecter)

@tree.command(name="easyt2i", description="less parameter mode")
async def easypaint(interaction: discord.Interaction):
    if authManagement.checkGuild(str(interaction.guild_id)):
        await interaction.response.send_modal(t2i_ui.createEasypaintui())
    else:
        await interaction.response.send_message("指揮官，這個伺服器沒有權限使用這個指令。請使用/help查看詳細說明", ephemeral=True)

@tree.command(name="detailt2i", description="detail parameter mode")
async def detailpaint(interaction: discord.Interaction):
    if authManagement.checkGuild(str(interaction.guild_id)):
        await interaction.response.send_modal(t2i_ui.createDetailpaintui())
    else:
        await interaction.response.send_message("指揮官，這個伺服器沒有權限使用這個指令。請使用/help查看詳細說明", ephemeral=True)

@tree.command(name="help", description="show the help message")
async def helpMsg(interaction: discord.Interaction):
    if interaction.user.dm_channel is None:
        await interaction.user.create_dm()
    await interaction.user.dm_channel.send(embed=HelpEmbedMessage(helpMessage))
    await interaction.response.send_message("協助指令已經送到您的信箱了!", ephemeral=True)

@tree.command(name="addguild", description="add auth guild to bot")
async def addGuild(interaction: discord.Interaction):
    if interaction.user.id == 337226622455513090:
        authManagement.addGuild(str(interaction.guild_id))
        await interaction.response.send_message(f"{interaction.guild.name} 已經加入!")
    else:
        await interaction.response.send_message("指揮官，你沒有權限使用這個指令。請使用/help查看詳細說明", ephemeral=True)

@tree.command(name="deleteguild", description="delete auth guild to bot")
async def deleteGuild(interaction: discord.Interaction):
    if interaction.user.id == 337226622455513090:
        authManagement.deleteGuild(str(interaction.guild_id))
        await interaction.response.send_message(f"{interaction.guild.name} 已經移除!")
    else:
        await interaction.response.send_message("指揮官，你沒有權限使用這個指令。請使用/help查看詳細說明", ephemeral=True)

@tree.command(name="changesd", description="change sd main model")
async def changesd(interaction: discord.Interaction):
    if interaction.user.id == 337226622455513090:
        if interaction.user.dm_channel is None:
            await interaction.user.create_dm()
        await interaction.user.dm_channel.send(view=discord.ui.View().add_item(select_ui(sdConnecter.getSDmodel(), sdConnecter.change_SDModel, "指揮官，模型已經修改成功!", callbacker2 = client.changeDisplayModel)))
        await interaction.response.send_message("修改指令已經送到您的信箱了!", ephemeral=True)
    else:
        await interaction.response.send_message("指揮官，你沒有權限使用這個指令。請使用/help查看詳細說明", ephemeral=True)

@client.event
async def on_message(message: discord.Message):
    if messageCommand.checkCommand(message.content):
        if authManagement.checkGuild(str(message.guild.id)):
            await messageCommand.performCommand(message)
        else:
            await message.reply("指揮官，這個伺服器沒有權限使用這個指令。請使用/help查看詳細說明")

client.run(variables["TOKEN"])