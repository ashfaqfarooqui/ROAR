#!/usr/bin/env python
import roslib;
import rospy
import json
from visualization_msgs.msg import *
from roar_msg.msg import *

import time
import threading 
from geometry_msgs.msg import Point

roslib.load_manifest('roar_bringup')

# objects:
class Robot:
    def __init__(self,robotName,position):
        self.initialPosition = position
        self.robotName = robotName
        self.pathPublisher = rospy.Publisher('path',Marker,queue_size=1)
        self.marker = Marker()
        self.marker.header.frame_id = "/neck"
        self.marker.type = self.marker.CUBE
        self.marker.action = self.marker.ADD
        self.marker.scale.x = 0.2
        self.marker.scale.y = 0.5
        self.marker.scale.z = 0.2
        self.marker.color.a = 1.0
        self.marker.color.r = 1.0
        self.marker.color.g = 1.0
        self.marker.color.b = 0.5
        self.marker.pose.orientation.w = 1.0
        self.marker.pose.position.x = position.x
        self.marker.pose.position.y = position.y
        self.marker.pose.position.z = position.z
        self.marker.lifetime = rospy.Duration(0.2)


    def getName(self):
        return self.robotName

    def  updatePosition(self, newPosition):
        self.marker.pose.position.x = newPosition.x
        self.marker.pose.position.y = newPosition.y
        self.marker.pose.position.z = newPosition.z

    def attachBin(self, bin):
        self.marker.color.a = 1.0
        self.marker.color.r = 1.0
        self.marker.color.g = 1.0
        self.marker.color.b = 1.0
        bin.setConnectedRobot(self)

    def dettachBin(self,bin):
        self.marker.color.a = 1.0
        self.marker.color.r = 1.0
        self.marker.color.g = 1.0
        self.marker.color.b = 0.5
        bin.disconnectRobot()

    def getMarker(self):
        return self.marker

    def getInitialPosition(self):
        return self.initialPosition

    def moveTo(self,obj):
        self.moveToDestination(obj.getInitialPosition())

    def moveToDestination(self, destination):
        self.lineList = Marker()
        self.lineList.header.frame_id = "/neck"
        self.lineList.type = self.marker.LINE_STRIP
        self.lineList.action = self.marker.ADD
        self.lineList.scale.x = 0.2
        self.lineList.scale.y = 0.5
        self.lineList.scale.z = 0.2
        self.lineList.color.a = 1.0
        self.lineList.color.r = 1.0
        self.lineList.color.g = 0.5
        self.lineList.color.b = 0.5
        self.lineList.pose.orientation.w = 1.0
        self.lineList.lifetime = rospy.Duration(5)
        self.lineList.points.append(self.marker.pose.position)
        self.lineList.points.append(destination)
        self.pathPublisher.publish(self.lineList)
        self.updatePosition(Point((self.marker.pose.position.x + destination.x)/2,(self.marker.pose.position.y + destination.y)/2,0))
        rospy.sleep(5)
        self.updatePosition(destination)

class Truck():
    def __init__(self,truckName,position):
        self.initialPosition = position
        self.truckName = truckName
        self.marker = Marker()
        self.marker.header.frame_id = "/neck"
        self.marker.type = self.marker.CUBE
        self.marker.action = self.marker.ADD
        self.marker.scale.x = 1.2
        self.marker.scale.y = 0.5
        self.marker.scale.z = 0.1
        self.marker.color.a = 1.0
        self.marker.color.r = 0.7
        self.marker.color.g = 0.3
        self.marker.color.b = 0.5
        self.marker.pose.orientation.w = 1.0
        self.marker.pose.position.x = position.x
        self.marker.pose.position.y = position.y
        self.marker.pose.position.z = position.z
        self.marker.lifetime = rospy.Duration(0.2)

    def getName(self):
        return self.truckName

    def getInitialPosition(self):
        return self.initialPosition

    def emptyBin(bin):
        bin.setEmptyStatus(True)

    def getMarker(self):
        return self.marker

class Bin(object):
    def __init__(self,binName,position):
        self.isEmpty = False
        self.initialPosition = position
        self.connectedRobot=None
        self.isAttached = False
        self.binName = binName
        self.marker = Marker()
        self.marker.header.frame_id = "/neck"
        self.marker.type = self.marker.CYLINDER
        self.marker.action = self.marker.ADD
        self.marker.scale.x = 0.2
        self.marker.scale.y = 0.2
        self.marker.scale.z = 0.5
        self.marker.color.a = 1.0
        self.marker.color.r = 1.0
        self.marker.color.g = 0.5
        self.marker.color.b = 0.5
        self.marker.pose.orientation.w = 1.0
        self.marker.pose.position.x = position.x
        self.marker.pose.position.y = position.y
        self.marker.pose.position.z = position.z
        self.marker.lifetime = rospy.Duration(0.2)
        self.__thread = threading.Thread(name=binName+"_thread", target=self.__keepAlive)
        self.__update_lock = threading.Lock()
        self.__thread.daemon = True
        self.__thread.start()

    def setEmptyStatus(self,status):
        self.marker.color.r = 0.5
        self.marker.color.g = 0.5
        self.marker.color.b = 0.5
        self.isEmpty = status

    def getEmptyStatus(self):
        return self.isEmpty

    def getName(self):
        return self.binName

    def getInitialPosition(self):
        return self.initialPosition

    def __keepAlive(self):
        while not rospy.is_shutdown():
            if self.isAttached == True:
                rospy.loginfo("Updating bin position")
                self.marker.pose.position.x = self.connectedRobot.marker.pose.position.x
                self.marker.pose.position.y = self.connectedRobot.marker.pose.position.y
                self.marker.pose.position.z = self.connectedRobot.marker.pose.position.z
            rospy.sleep(0.1)

    def getPosition(self):
        return self.marker.pose.position

    def setConnectedRobot(self,robot):
        self.isAttached = True
        self.connectedRobot = robot

    def disconnectRobot(self):
        self.setConnectedRobot(None)
        self.isAttached = False

    def getMarker(self):
        return self.marker


# simulation
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
                    try:
                        tasks = evt.Event.split("_")
                        methodToCall = getattr(self.getObject(tasks[0]),tasks[1])
                        methodToCall(self.getObject(tasks[2]))
                    except Exception, e:
                        rospy.loginfo(e)
                    finally:
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

