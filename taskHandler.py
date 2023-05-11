class taskHandler():
    def __init__(self, paintClass):
        self.queue = list()

    def addTask(self, task):
        self.queue.append(task)

    def removeTask(self):
        return self.queue.pop(0)
    
    def performTask(self):

class task():
    def __init__(self, )
