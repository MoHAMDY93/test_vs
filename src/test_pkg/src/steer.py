#! /bin/env python3

import rospy
from std_msgs.msg import Float64

steer_pub = rospy.Publisher("/SteeringAngle" , Float64 , queue_size=2)

rospy.init_node("steering")

def car_steer(angle: float):
    steer_pub.publish(angle)

if(__name__ == '__main__'):
    rate = rospy.Rate(10)
    while(not rospy.is_shutdown()):
        steering_angle = rospy.get_param("/steering_angle")
        car_steer(steering_angle)
        rate.sleep()

    rospy.loginfo("Stopped Publishing ... c u😘")
    