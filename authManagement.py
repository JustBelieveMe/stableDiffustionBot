import json

class authManagement():
    def __init__(self) -> None:
        try:
            with open("./authGuild.json", "r", encoding="utf-8") as authGuildFile:
                self.authGuild = json.load(authGuildFile)["authGuild"]
                self.authGuildList = self.authGuild.keys()
        except OSError:
            raise "ERROR: there is no authGuild.json"
        
    def getGuildList(self):
        return self.authGuild

    def checkGuild(self, guildID: str) -> bool:
        if guildID in self.authGuildList:
            return True
        else:
            return False

    def addGuild(self, guildID: str) -> bool:
        if not self.checkGuild(guildID):
            self.authGuild[guildID] = 0
            data = {"authGuild":self.authGuild}
            self.changeAuthGuildJson(data)
            return True
        else:
            return False

    def deleteGuild(self, guildID: str) -> bool:
        if self.checkGuild(guildID):
            del self.authGuild[guildID]
            data = {"authGuild":self.authGuild}
            self.changeAuthGuildJson(data)
            return True
        else:
            return False

    def changeAuthGuildJson(self, data) -> None:
        try:
            with open("./authGuild.json", "w", encoding="utf-8") as authGuildFile:
                newJson = json.dumps(data)
                authGuildFile.write(newJson)
        except OSError:
            print("ERROR: authGuild.json change file fail!")