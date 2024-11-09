#! /bin/env python3

import rospy
from std_msgs.msg import Float64
from nav_msgs.msg import Odometry

test = None

def odometry_callback(data):
    rospy.loginfo(f"HOLA LIL BROTHERS")
    
# Initialize ROS node with the name "track_1"
rospy.init_node("test")


third_pup = rospy.Publisher("/test", Float64, queue_size=1)

# Subscribe to the odometry topic to track the car's position
rospy.Subscriber('/odom', Odometry, odometry_callback)

if __name__ == '__main__':
    while(True):
        rospy.set_param("/padel" , 0.2)
        rospy.set_param("/steering_angle" , 18.5)
    