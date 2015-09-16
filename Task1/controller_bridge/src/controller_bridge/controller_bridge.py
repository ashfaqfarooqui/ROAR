import requests


class ControllerBridge:

    """docstring for controller_bridge"""

    __bridgeInstance = None
    __currentUID = 0

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.url = "http://" + str(self.host) + ":" + str(self.port) + "/api/ts"

    def getExecutingOperations(self):
        exeOps = []
        tsJson = self.getTSData()
        self.__setCurrentID(tsJson.get("id"))
        allOperations = tsJson.get("operations")
        for operation in allOperations:
            if operation.get('executing') == "true":
                exeOps.append(operation.get('name'))
        return exeOps

    def getTSData(self):
        transitions = requests.get(self.url)
        return transitions.json()

    def __setCurrentID(self, id):
        self.__currentUID = id

    def getCurrentID(self):
        return self.__currentUID

    def postTransition(self, ts):
        requests.post(self.url+"/transition", ts)

    @staticmethod
    def getInstance(host='localhost', port="8080"):
        if ControllerBridge.__bridgeInstance is None:
            print "instance"
            ControllerBridge.__bridgeInstance = ControllerBridge(host, port)
        return ControllerBridge.__bridgeInstance
