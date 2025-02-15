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

MAX_JOINT_VALUE = 0.78539816339
MIN_JOINT_VALUE = -0.78539816339

jointValue = MIN_JOINT_VALUE
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
        jointValue += 0.005
    elif req.directionToMove == "up":
        global jointValue
        jointValue -= 0.005
    if(jointValue > MAX_JOINT_VALUE):
        jointValue = MAX_JOINT_VALUE
    elif(jointValue < MIN_JOINT_VALUE):
        jointValue = MIN_JOINT_VALUE
    return True

class LiftMovement(object):
    # create messages that are used to publish feedback/result
    _feedback = lift_msgs.msg.LiftMovementFeedback()
    _result = lift_msgs.msg.LiftMovementResult()

    def __init__(self, name):
        self._action_name = name
        self._as = actionlib.SimpleActionServer(self._action_name, lift_msgs.msg.LiftMovementAction, execute_cb=self.execute_cb, auto_start = False)
        self._as.start()
        
    def isGoalReached(self,goal):
        if (goal == "up" and jointValue == -0.78539816339) or (goal == "down" and jointValue == 0.78539816339):
            return True
        else:
            return False

    def execute_cb(self, goal):
        # Fill in code here 
        goal = goal.direction
        print "Goal recieved"
        print goal
        self.success = self.isGoalReached(goal)

        while self.isGoalReached(goal) == False:
            rospy.wait_for_service('Simulate_Lift')
            try:
                simulate_lift = rospy.ServiceProxy('Simulate_Lift', SimulateLift)
                resp1 = simulate_lift(goal)
            except rospy.ServiceException, e:
                print "Service call failed: %s"%e
            self.success = self.isGoalReached(goal)
            if self._as.is_preempt_requested():
                rospy.loginfo('%s: Preempted' % self._action_name)
                self._as.set_preempted()
                self.success = False
            rospy.sleep(0.015)
        if self.success:
          self._result.success = self.success
          rospy.loginfo('%s: Succeeded' % self._action_name)
          self._as.set_succeeded(self._result)


if __name__ == '__main__':
    LiftMovement('LiftMovementActionServer')
    main()
