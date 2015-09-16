#!/usr/bin/env python
import roslib;
import rospy
import time
import sys
from visualization_msgs.msg import *
import threading 
from geometry_msgs.msg import Point

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
        rospy.loginfo("Updating position")
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

    def moveToBin(self,bin):
        self.moveToDestination(bin.getInitialPosition())

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
    def __init__(self,position):
        self.initialPosition = position
        self.connectedRobot=None
        self.isAttached = False
        self.marker = Marker()
        self.marker.header.frame_id = "/neck"
        self.marker.type = self.marker.CUBE
        self.marker.action = self.marker.ADD
        self.marker.scale.x = 0.5
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
        return self.binName

    def getInitialPosition(self):
        return self.initialPosition

    def emptyBin(bin):
        bin.setEmpty(True)

    def getMarker(self):
        return self.marker

class Bin(object):
    def __init__(self,binName,position):
        self.isEmpty = False
        self.initialPosition = position
        self.connectedRobot=None
        self.isAttached = False
        self.binName = binName
        # self.publisher = rospy.Publisher(binName+'_marker',Marker,queue_size=1)
        self.marker = Marker()
        self.marker.header.frame_id = "/neck"
        self.marker.type = self.marker.CYLINDER
        self.marker.action = self.marker.ADD
        self.marker.scale.x = 0.2
        self.marker.scale.y = 0.2
        self.marker.scale.z = 0.5
        self.marker.color.a = 1.0
        self.marker.color.r = 1.0
        self.marker.color.g = 1.0
        self.marker.color.b = 0.5
        self.marker.pose.orientation.w = 1.0
        self.marker.pose.position.x = position.x
        self.marker.pose.position.y = position.y
        self.marker.pose.position.z = position.z
        self.marker.lifetime = rospy.Duration(0.2)
        # self.publisher.publish(self.marker)
        self.__thread = threading.Thread(name=binName+"_thread", target=self.__keepAlive)
        self.__update_lock = threading.Lock()
        self.__thread.daemon = True
        self.__thread.start()

    def setEmpty(self,status):
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
