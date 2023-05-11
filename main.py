#  https://discordapp.com/oauth2/authorize?&client_id=772092610104918017&scope=bot&permissions=8

import discord
import json
from botClient import botClient
from ui.t2i_ui import Easypaint, Detailpaint
from ui.userChange_ui import AddUser, DeleteUser
from paintClass import paintClass
from userManagement import userManagement

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.messages = True
intents.members = True

with open("./variables.json", "r", encoding="utf-8") as variableFile:
    variables = json.load(variableFile)

with open("./helpMsg.txt", "r", encoding='utf-8') as helpMsgFile:
    helpMsgRaw = helpMsgFile.readlines()
    helpMesg = str()
    for line in helpMsgRaw:
        helpMesg += line

client = botClient(intents)
tree = client.getTree()
painter = paintClass()
userManagement = userManagement()

@tree.command(name="easypaint", description="less parameter mode")
async def easypaint(interaction: discord.Interaction):
    if userManagement.checkUser(interaction.user.id):
        await interaction.response.send_modal(Easypaint(painter))
    else:
        await interaction.response.send_message("指揮官，你沒有權限使用這個指令。", ephemeral=True)

@tree.command(name="detailpaint", description="detail parameter mode")
async def detailpaint(interaction: discord.Interaction):
    if userManagement.checkUser(interaction.user.id):
        await interaction.response.send_modal(Detailpaint(painter))
    else:
        await interaction.response.send_message("指揮官，你沒有權限使用這個指令。", ephemeral=True)

@tree.command(name="help", description="show the help message")
async def helpMsg(interaction: discord.Interaction):
    if interaction.user.dm_channel is None:
        await interaction.user.create_dm()
    await interaction.user.dm_channel.send(helpMesg)
    await interaction.response.send_message("協助指令已經送到您的信箱了!", ephemeral=True)

@tree.command(name="adduser", description="add auth user to bot")
async def adduser(interaction: discord.Interaction):
    if interaction.user.id == 337226622455513090:
        await interaction.response.send_modal(AddUser(userManagement, client.get_user))
    else:
        await interaction.response.send_message("指揮官，你沒有權限使用這個指令。", ephemeral=True)

@tree.command(name="deleteuser", description="delete auth user to bot")
async def deleteuser(interaction: discord.Interaction):
    if interaction.user.id == 337226622455513090:
        await interaction.response.send_modal(DeleteUser(userManagement, client.get_user))
    else:
        await interaction.response.send_message("指揮官，你沒有權限使用這個指令。", ephemeral=True)

# @tree.command(name="adduser", description="add user to authUser.json")

client.run(variables["TOKEN"])