#! /bin/env python3

# This File is for the main track but with using the total distance as or controller, didn't use yaw.
import rospy
from std_msgs.msg import Float64
from nav_msgs.msg import Odometry
import math

start_x = None
start_y = None
total_distance = 0.0
previous_x = None
previous_y = None

def odometry_callback(data):
    global start_x, start_y, total_distance, previous_x, previous_y

    current_x = data.pose.pose.position.x
    current_y = data.pose.pose.position.y

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
    
rospy.init_node("work")


work_pup = rospy.Publisher("/work", Float64, queue_size=1)

start_time = rospy.get_rostime().secs

rospy.Subscriber('/odom', Odometry, odometry_callback)

# To go into a circle we gonna use the Turning Radius equation in which we have to know the follwing information :
# R = L / (tan(theta)) 

# 1) Wheelbase (L): The distance between the front and rear wheels.
# 2) Steering angle(theta) -> this is the missing one

# so by simple math we can know the steering angle we turn with

# Now, when to stop ?!!
# There are two approaches :

# first)    when the car reaches the start position(start_x & start_y) once again we should stop -> Failed
# The position is in float pointing format so we can't using comparison with it, tried to approximate it but failed in it too😑

# second)   Simply compute the circumference(2 * PI * R) of the track and when the total distance reaches it we stop -> AC☝️

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
        
def make_full_circle(r , l , curr_distance):
    steering = math.atan(l / r) * (180 / math.pi)
    circumfarence = math.ceil(2 * math.pi * r)
    rospy.set_param("/padel" , 0.2)
    rospy.set_param("/steering_angle" , steering)
    while(True):
        rospy.loginfo(f"Steerinig: {steering} , Circumfarence: {circumfarence}")
        if(curr_distance - total_distance < circumfarence / 2):
            rospy.set_param("/padel" , 0.2)
        else:
            rospy.set_param("/padel" , 0.1)
        rospy.set_param("/steering_angle" , steering)
        if(total_distance - curr_distance > circumfarence):
            break
    
if __name__ == '__main__':
    curr = total_distance
    move(50 , curr)

    curr = total_distance
    make_full_circle(6.0 , 2.269 , curr)
    
    #  Then أرفع رجلك من ع البنزين
    rospy.set_param("/padel", 0.0)
    # ودوس ع الفرامل براحة عشان العربية متتدريفتش مننا
    rospy.set_param("/brakes", 0.2)
    rospy.loginfo("-------------------------------------------")
    rospy.loginfo(f"Car has moved {total_distance} meters.")
    rospy.loginfo(f"Total Time: {rospy.get_rostime().secs - start_time}\n")
    rospy.loginfo("Work is Done :).\n")
    
# Log a message indicating the shutdown of the node
rospy.loginfo("Shutdown requested. Exiting...")
