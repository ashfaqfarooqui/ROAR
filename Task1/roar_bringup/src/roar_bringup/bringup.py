#!/usr/bin/env python
import roslib;
import rospy
import json
from roar_bringup.robot import *
from visualization_msgs.msg import *
from roar_msg.msg import *

roslib.load_manifest('roar_bringup')

class Simulation:

    def __init__(self):
        self.evtList = []
        self.publisher = rospy.Publisher('Markers',MarkerArray,queue_size=10)
        rospy.Subscriber('Events', Event, self.callbackEventMsg)
        self.uc_eventPublisher = rospy.Publisher('uc_Events', Event, queue_size=5)
        self.markerArray = MarkerArray()
        self.__thread = None
        self.objArray = []


    def callbackEventMsg(self,evt):
        self.evtList.append(evt)

    def initScene(self):
        
        with open(roslib.packages.get_pkg_dir('roar_bringup')+'/config.json') as configFile:
            config = json.load(configFile)

        for val in config:
            if val.get("Obj") == "Robot":
                pos = val.get("Position")
                robot = Robot(val.get("Name"),Point(pos[0],pos[1],pos[2]))
                self.objArray.append(robot)
                self.markerArray.markers.append(robot.getMarker())
            elif val.get("Obj") == "Bin":
                pos = val.get("Position")
                bin = Bin(val.get("Name"),Point(pos[0],pos[1],pos[2]))
                self.objArray.append(bin)
                self.markerArray.markers.append(bin.getMarker())
            elif val.get("Obj") == "Truck":
                pos = val.get("Position")
                truck = Truck(val.get("Name"),Point(pos[0],pos[1],pos[2]))
                self.markerArray.markers.append(truck.getMarker())
                self.objArray.append(truck)


        self.__thread = threading.Thread(name="keepAliveThread", target=self.__keepAlive)
        self.__update_lock = threading.Lock()
        self.__thread.daemon = True
        self.__thread.start()



    def __keepAlive(self):
        while not rospy.is_shutdown():
            id = 0;
            for markers in self.markerArray.markers:
                markers.header.stamp = rospy.get_rostime()
                markers.id = id
                id += 1
            self.publisher.publish(self.markerArray)
            rospy.sleep(0.1)

    def main(self):
        rospy.init_node("SceneManager")
        self.initScene()
        while not rospy.is_shutdown():
            if self.evtList.__len__() > 0:
                for evt in self.evtList:
                    tasks = evt.Event.split("_")
                    methodToCall = getattr(self.getObject(tasks[0]),tasks[1])
                    methodToCall(self.getObject(tasks[2]))
                    self.sendUCEvent(evt)
            rospy.sleep(0.1)


    def getObject(self,name):
        for obj in self.objArray:
            if obj.getName() == name:
                return obj

    def sendUCEvent(self,evt):
        uc_eventMsg = Event()
        uc_eventMsg.Event = "uc_" + evt.Event
        uc_eventMsg.UID = evt.UID
        self.uc_eventPublisher.publish(uc_eventMsg)
        self.evtList.pop(0)

if __name__ == '__main__':
    sim = Simulation()
    sim.main()

