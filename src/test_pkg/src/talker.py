#! /bin/env python3

import rospy
from std_msgs.msg import String

def talker():
    pub = rospy.Publisher('/chatter', String, queue_size=10)
    
    rospy.init_node('talker_node', anonymous=True)

    rate = rospy.Rate(1)

    while not rospy.is_shutdown():
        # Create a message
        hello_str = "Hello ROS! Time: %s" % rospy.get_time()
        # Log the message
        # rospy.loginfo(hello_str)
        # Publish the message
        pub.publish(hello_str)
        # Sleep to maintain the loop rate
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
