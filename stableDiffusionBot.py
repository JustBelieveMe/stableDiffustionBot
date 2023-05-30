import discord
import json
import requests
import io
import asyncio
import base64
from PIL import Image, PngImagePlugin

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.messages = True
intents.message_content = True
intents.members = True

client = discord.Client(intents = intents)
with open("./variables.json", "r") as variableFile:
    variables = json.load(variableFile)
    print("variable loaded successfully")

with open("./authUser.json", "r") as authUserFile:
    authUser = json.load(authUserFile)["authUser"]
    print("auth user loaded successful")

with open("./payload.json", "r") as payloadFile:
    payload = json.load(payloadFile)

with open("./defaultPrompt.json", "r") as defaultPromptFile:
    defaultPrompt = json.load(defaultPromptFile)
    print("defaultPrompt loaded successfully")

async def easypaint(message, command_dict, payload, defaultPrompt):
    payload["prompt"] = command_dict["prompt"]
    payload["negative_prompt"] = defaultPrompt["negative_prompt"]
    payload["batch_size"] = defaultPrompt["batch_size"]
    txt2img(message, command_dict, payload)
    return

async def txt2img(message, command_dict, payload):
    url=f'{StableDiffurl}/sdapi/v1/txt2img'
    print(url)
    response = requests.post(url=url, json=payload)
    r = response.json()
    print(r)
    for i in r['image']:
        with io.BytesIO(base64.b64decode(i.split(",", 1)[0])) as image_binary:
            # image.save(image_binary, 'PNG')
            image_binary.seek(0)
            await message.reply(file=discord.File(fp=image_binary), filename='image.png')
        
def commandHelper(message):
    commands = message.content.split("-")
    print(f"user{message.author} use {commands[0]}")
    command_dict = dict()
    for command in commands:
        seper = command.split(" ", 1)
        if len(seper) == 1:
            continue
        command_dict[seper[0]] = seper[1]
    return command_dict

if __name__ == "__main__":    
    StableDiffurl = "http://127.0.0.1:5411"
    loop = asyncio.get_event_loop() #建立一個Event Loop
    loop.run_forever()
    @client.event
    async def on_ready():
        print('已連接到Discord，機器人已啟動！')

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        if message.content.startswith('!easypaint'):
            if message.author.id not in authUser:
                print(f"user {message.author}({message.author.id}) try to use command")
                return
            await easypaint(message, commandHelper(message), payload, defaultPrompt)
            

    client.run(variables["TOKEN"])