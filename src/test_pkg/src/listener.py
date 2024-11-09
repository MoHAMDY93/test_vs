#! /bin/env python3

import rospy
from std_msgs.msg import String

def callback(data):
    # Log the received message
    rospy.loginfo("I heard: %s", data.data)

def listener():
    # Initialize the node
    rospy.init_node('listener_node', anonymous=True)
    # Create a subscriber object
    # rospy.Subscriber('/chatter', String, callback): Subscribes to the /chatter topic using the String message type.
    # callback(data): Called whenever a new message is received on /chatter.
    rospy.Subscriber('/chatter', String, callback)
    # Keep the node running
    rospy.spin()

if __name__ == '__main__':
    listener()
