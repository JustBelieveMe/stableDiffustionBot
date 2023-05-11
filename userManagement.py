import json

class userManagement():
    def __init__(self) -> None:
        try:
            with open("./authUser.json", "r", encoding="utf-8") as authUserFile:
                self.authUser = json.load(authUserFile)["authUser"]
        except OSError:
            raise "ERROR: there is no authUser.json"
        
    def checkUser(self, userID) -> bool:
        if userID in self.authUser:
            return True
        else:
            return False

    def addUser(self, userID: int) -> bool:
        if not self.checkUser(userID):
            self.authUser.append(userID)
            data = {"authUser":self.authUser}
            self.changeAuthUserJson(data)
            return True
        else:
            return False

    def deleteUser(self, userID: int) -> bool:
        if self.checkUser(userID):
            self.authUser.remove(userID)
            data = {"authUser":self.authUser}
            self.changeAuthUserJson(data)
            return True
        else:
            return False

    def changeAuthUserJson(self, data) -> None:
        try:
            with open("./authUser.json", "w", encoding="utf-8") as authUserFile:
                newJson = json.dumps(data)
                authUserFile.write(newJson)
        except OSError:
            print("ERROR: auth user change file fail!")