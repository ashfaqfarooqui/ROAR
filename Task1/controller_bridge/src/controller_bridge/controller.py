#!/usr/bin/env python
import roslib
import rospy
import optparse


from roar_msg.msg import Event
from controller_bridge.controller_bridge import ControllerBridge

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

if __name__ == '__main__':
    main()
