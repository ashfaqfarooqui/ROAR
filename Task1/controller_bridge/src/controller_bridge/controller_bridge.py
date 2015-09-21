#!/usr/bin/env python
import roslib
import rospy
import optparse

import requests



from roar_msg.msg import Event

roslib.load_manifest('controller_bridge')
activeOperations = []


def callbackupEventMsg(uc_evt):
    rospy.loginfo("UC evt recieved:" + uc_evt.Event)
    ControllerBridge.getInstance().postTransition(uc_evt.Event)
    print uc_evt.Event[3:]
    activeOperations.remove(uc_evt.Event[3:])


def main():

    UID = lastUID = 0
    # Parses command line arguments
    parser = optparse.OptionParser(usage="usage: %prog hostname port")
    (options, args) = parser.parse_args(rospy.myargv()[1:])
    if len(args) < 1:
        controller_hostname = 'localhost'
        port = 8080
    elif len(args) == 1:
        controller_hostname = args[0]
        port = 8080
    elif len(args) == 2:
        controller_hostname = args[0]
        port = int(args[1])
        if not (0 <= port <= 65535):
                parser.error("You entered an invalid port number")
    else:
        parser.error("Wrong number of parameters")

    rospy.init_node('ControllerBridge')
    rate = rospy.Rate(2)
    eventPublisher = rospy.Publisher('Events', Event, queue_size=5)
    rospy.Subscriber('uc_Events', Event, callbackupEventMsg)
    cb = ControllerBridge.getInstance(controller_hostname,port)
    while not rospy.is_shutdown():
        lastUID = UID
        operations = cb.getExecutingOperations()
        UID = cb.getCurrentID()
        if UID != lastUID:
            for operation in operations:
                if operation not in activeOperations:
                    eventMsg = Event()
                    eventMsg.Event = operation
                    eventMsg.UID = UID
                    rospy.loginfo(eventMsg)
                    eventPublisher.publish(eventMsg)
                    rospy.loginfo("operation completed with UID:" + str(UID))
                    activeOperations.append(operation)
        rate.sleep()


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

if __name__ == '__main__':
    main()
