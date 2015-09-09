#!/usr/bin/env python
import roslib
import rospy
import time
import sys
from roar_msg.srv import *
from sensor_msgs.msg import JointState


roslib.load_manifest('simulate_lift')
rospy.init_node('simulate_lift')



jointValue = -0.78539816339
def main():
    jointStatePub = rospy.Publisher('joint_states', JointState, queue_size=5)
    rospy.Service('Simulate_Lift', SimulateLift, handleSimulateLift)
    rate = rospy.Rate(125)
    while not rospy.is_shutdown():
        msg = JointState()
        msg.header.stamp = rospy.Time.now()
        msg.name=['right_leg_right_arm','left_leg_left_arm']
        msg.position=[jointValue,jointValue]
        msg.velocity = []
        msg.effort = []
        jointStatePub.publish(msg)
        rate.sleep()


def handleSimulateLift(req):
    if req.directionToMove == "down":
        global jointValue
        jointValue += 0.1
    elif req.directionToMove == "up":
        global jointValue
        jointValue -= 0.1
    if(jointValue > 0.78539816339):
        jointValue = 0.78539816339
    elif(jointValue < -0.78539816339):
        jointValue = -0.78539816339
    return True

if __name__ == '__main__':
    main()
