#! /bin/env python3

# This one for the U-turn Track ofc by suign the yaw.  
import rospy
import math
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion
from std_msgs.msg import Float64

def get_yaw(orientation_q):
    orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
    _, _, yaw = euler_from_quaternion(orientation_list)
    return yaw


initial_yaw = None
total_change = 0.0
start_x = None
start_y = None
total_distance = 0.0
previous_x = None
previous_y = None

def odom_callback(msg): 
    global start_x, start_y, total_distance, previous_x, previous_y

    current_x = msg.pose.pose.position.x
    current_y = msg.pose.pose.position.y

    if start_x is None and start_y is None:
        start_x = current_x
        start_y = current_y

    if previous_x is None and previous_y is None:
        previous_x = current_x
        previous_y = current_y

    distance_traveled = math.sqrt((current_x - previous_x) ** 2 + (current_y - previous_y) ** 2)

    total_distance += distance_traveled

    previous_x = current_x
    previous_y = current_y

    rospy.loginfo(f"Total Distance Moved: {total_distance} meters")
    
    global initial_yaw , total_change
    current_yaw = get_yaw(msg.pose.pose.orientation)
    if initial_yaw is None:
        initial_yaw = current_yaw
        return
    
    yaw_diff = current_yaw - initial_yaw
    
    if yaw_diff > math.pi:
        yaw_diff -= 2 * math.pi
    elif yaw_diff < -math.pi:
        yaw_diff += 2 * math.pi

    total_change += yaw_diff

    initial_yaw = current_yaw
    rospy.loginfo(f"total change: {total_change}")

yaw_pup = rospy.Publisher("/yaw", Float64, queue_size=1)

rospy.init_node("yaw")
# Subscribe to odometry topic
rospy.Subscriber("/odom", Odometry, odom_callback)

def move(distance , curr_distance):
    rospy.set_param("/steering_angle" , 0.0)    
    while(True):
        rospy.set_param("/steering_angle" , 0.0)    
        rospy.set_param("/padel" , 0.5)
        if(total_distance - curr_distance > distance / 2):
            break
    
    while(True):
        rospy.set_param("/steering_angle" , 0.0)    
        rospy.set_param("/padel" , 0.2)
        if(total_distance - curr_distance > distance):
            break
    rospy.set_param("/padel" , 0.0)

def test_yaw(curr_change):
    correction_factor = 0.25
    while(True):
        rospy.set_param("/padel", 0.2)
        rospy.set_param("/steering_angle", 18)
        if(curr_change + correction_factor > math.pi):
            break
        curr_change = total_change

if __name__ == '__main__':
    
    curr = total_distance
    move(50 , curr)
    
    curr_cha = total_change
    test_yaw(curr_cha)
    # while(not completed):
    #     rospy.set_param("/padel", 0.2)
    #     rospy.set_param("/steering_angle", 18)
    
    curr = total_distance
    move(50 , curr)
    
    rospy.set_param("/padel", 0.0)
    rospy.set_param("/brakes", 0.2)
        