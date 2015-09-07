#!/usr/bin/env python
import roslib
import rospy
import time
import sys
from ROAR_msgs import *
from sensor_msgs import JointState


roslib.load_manifest('simulate_lift')

jointStatePub = rospy.Publisher('Joint_state',JointState,1)

jointValue = 0
def main():
    rospy.init_node('simulate_lift')
    rospy.Service('Simulate_Lift', SimulateLift, handleSimulateLift)

    rospy.Subscriber('robot_state_publisher',callbackRSP)
    rospy.spin()

def callbackRSP(msg):
    global jointValue
    jointValue = msg.position(1)


def handleSimulateLift(req):
    msg = JointState()
    jointVal = jointValue
    if req.directionToMove == "up":
        msg.name.append('right_leg_right_arm')
        msg.name.append('left_leg_left_arm')
        jointVal += 0.05
        msg.position.append(jointVal)
        msg.position.append(jointVal)
        jointStatePub.publish(msg)
        return True
    else req.directionToMove == "down":
        if req.directionToMove == "up":
        msg.name.append('right_leg_right_arm')
        msg.name.append('left_leg_left_arm')
        jointVal += 0.05
        msg.position.append(jointVal)
        msg.position.append(jointVal)
        jointStatePub.publish(msg)
        return True
    return False

if __name__ == '__main__':
    main()
