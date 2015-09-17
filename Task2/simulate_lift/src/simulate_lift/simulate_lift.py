#!/usr/bin/env python
import roslib
import rospy
import time
import sys
from lift_msgs.srv import *
from lift_msgs.msg import *
from sensor_msgs.msg import JointState
import actionlib

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

class LiftMovement(object):
    # create messages that are used to publish feedback/result
    _feedback = lift_msgs.msg.LiftMovementFeedback()
    _result = lift_msgs.msg.LiftMovementResult()

    def __init__(self, name):
        self._action_name = name
        self._as = actionlib.SimpleActionServer(self._action_name, lift_msgs.msg.LiftMovementAction, execute_cb=self.execute_cb, auto_start = False)
        self._as.start()
        
    def execute_cb(self, goal):
        # Fill in code here 
      self._result.success = True
      self._as.set_succeeded(self._result)

if __name__ == '__main__':
    main()
