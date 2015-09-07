#!/usr/bin/env python
import roslib
import rospy
import time
import sys
from visualization_msgs import *

roslib.load_manifest('roar_bringup')


def main():
    rospy.init_node('roar_bringup')
    markerPublisher = rospy.Publisher('markers', Event, queue_size=5)
    rospy.spin()




if __name__ == '__main__':
    main()
