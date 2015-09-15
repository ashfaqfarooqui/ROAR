#!/usr/bin/env python
import roslib;
import rospy
import time
import sys
from interactive_markers.interactive_marker_server import *
from visualization_msgs.msg import *
import threading 
from geometry_msgs.msg import Point


roslib.load_manifest('roar_bringup')


class robot:
    def __init__(self,robotName,position = Point(0,0,0)):
        self.publisher = rospy.Publisher(robotName+'_marker',Marker,queue_size=1)
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
        self.marker.pose.position.x = 0
        self.marker.pose.position.y = 0
        self.marker.pose.position.z = 0
        self.marker.lifetime = rospy.Duration(0.1)
        self.publisher.publish(self.marker)
        self.__thread = threading.Thread(name=robotName+"_thread", target=self.__keepAlive)
        self.__update_lock = threading.Lock()
        self.__thread.daemon = True
        self.__thread.start()

    def __keepAlive(self):
        while not rospy.is_shutdown():
            rospy.loginfo("Publishing message")
            self.publisher.publish(self.marker)
            rospy.sleep(0.1)

    def  updatePosition(self, newPosition):
        rospy.loginfo("Updating position")
        self.marker.pose.position.x = newPosition.x
        self.marker.pose.position.y = newPosition.y
        self.marker.pose.position.z = newPosition.z

    def attachBin(self, bin):
        bin.setConnectedRobot(self)

    def dettachBin(self,bin):
        bin.disconnectRobot()

    def getMarker(self):
        return self.marker

    def move(self, destination):
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
        rospy.sleep(3)
        self.updatePosition(destination)


class Bin(object):
    def __init__(self,binName,position = Point(0,0,0)):
        self.connectedRobot=None
        self.isAttached = False
        self.publisher = rospy.Publisher(binName+'_marker',Marker,queue_size=1)
        self.marker = Marker()
        self.marker.header.frame_id = "/neck"
        self.marker.type = self.marker.CYLINDER
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
        self.marker.lifetime = rospy.Duration(0.1)
        self.publisher.publish(self.marker)
        self.__thread = threading.Thread(name=binName+"_thread", target=self.__keepAlive)
        self.__update_lock = threading.Lock()
        self.__thread.daemon = True
        self.__thread.start()

    def __keepAlive(self):
        while not rospy.is_shutdown():
            if self.isAttached == True:
                rospy.loginfo("Updating position")
                self.marker.pose.position.x = self.connectedRobot.marker.pose.position.x+0.1
                self.marker.pose.position.y = self.connectedRobot.marker.pose.position.y
                self.marker.pose.position.z = self.connectedRobot.marker.pose.position.z
            rospy.loginfo("Publishing message")
            self.publisher.publish(self.marker)
            rospy.sleep(0.1)


    def getPosition(self):
        return self.marker.pose.position

    def setConnectedRobot(self,robot):
        self.isAttached = True
        self.connectedRobot = robot

    def disconnectRobot(self):
        self.setConnectedRobot(None)
        self.isAttached = False



if __name__ == '__main__':
    position = Point(0, 0 ,0)
    rospy.init_node("SceneManager")
    rob = robot("Robot1",position)
    bin1 = Bin("Bin1",Point(5,4,0))
    rospy.sleep(10)
    rob.move(Point(5,4,0))
    rospy.sleep(20)
    rob.dettachBin(bin1)
    while not rospy.is_shutdown():
        rospy.sleep(0.1)

