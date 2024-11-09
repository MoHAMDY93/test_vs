#! /bin/env python3

import rospy
from std_msgs.msg import Float64

cmd_vel_pup = rospy.Publisher("/cmd_vel" , Float64 , queue_size = 1)

rospy.init_node("move")

def move_car(padel: float):
    cmd_vel_pup.publish(padel)

if __name__ == '__main__': 
    rate = rospy.Rate(10)

    while (not rospy.is_shutdown()):
        padel = rospy.get_param("/padel")
        move_car(padel)
        rate.sleep()
    
    rospy.loginfo("Stopped Publishing ... c u😘")