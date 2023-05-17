import discord
from discord.ui import Select

class select_ui(Select):
    def __init__(self, optionList, callbacker1, callback_message, callbacker2 = None):
        self.callbacker1 = callbacker1
        self.callbacker2 = callbacker2
        self.optionList = optionList
        self.callback_message = callback_message
        self.SelectMenuOptionList = list()
        for selection in self.optionList:
            self.SelectMenuOptionList.append(discord.SelectOption(label=selection, value=selection))
        super().__init__(options=self.SelectMenuOptionList)

    async def callback(self, interaction):
        await interaction.response.defer(thinking=True)
        self.callbacker1(self.values[0])
        if self.callbacker2 is not None:
            await self.callbacker2(self.values[0])
        await interaction.followup.send(self.callback_message)
        
        