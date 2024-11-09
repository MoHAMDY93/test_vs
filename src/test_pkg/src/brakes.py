#! /bin/env python3

import rospy
from std_msgs.msg import Float64

brakes_pub = rospy.Publisher("/brakes" , Float64 , queue_size=2)

rospy.init_node("brakes")

def car_brake(brakes_value: float):
    brakes_pub.publish(brakes_value)

if(__name__ == '__main__'):
    rate = rospy.Rate(10)

    while(not rospy.is_shutdown()):
        brakes = rospy.get_param("/brakes")
        car_brake(brakes)
        rate.sleep()

    rospy.loginfo("Stopped Publishing ... c u😘")