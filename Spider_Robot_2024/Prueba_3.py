#!/usr/bin/env python

import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from geometry_msgs.msg import Pose, Point, Quaternion

def move_to_goal(x, y, z, qx, qy, qz, qw):
    rospy.init_node('send_goal_node', anonymous=True)
    
    client = actionlib.SimpleActionClient('/jethexa/move_base', MoveBaseAction)
    
    rospy.loginfo("Waiting for move_base action server...")
    client.wait_for_server()
    
    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "jethexa/map"
    goal.target_pose.header.stamp = rospy.Time.now()
    
    goal.target_pose.pose = Pose(Point(x, y, z), Quaternion(qx, qy, qz, qw))
    
    rospy.loginfo("Sending goal: (%s, %s, %s) with orientation (%s, %s, %s, %s)", x, y, z, qx, qy, qz, qw)
    client.send_goal(goal)
    
    wait = client.wait_for_result()
    if not wait:
        rospy.logerr("Action server not available! Could not get result from move_base.")
        rospy.signal_shutdown("Action server not available!")
    else:
        return client.get_result()

def leer_coordenadas(archivo):
    puntos = []
    with open(archivo, 'r') as f:
        for linea in f:
            if linea.strip() and not linea.startswith('#'):
                valores = [float(valor) for valor in linea.split()]
                puntos.append(valores)
    return puntos

if __name__ == '__main__':
    try:
        coordenadas = leer_coordenadas('./coordenadas.txt')
        for punto in coordenadas:
            x, y, z, qx, qy, qz, qw = punto
            result = move_to_goal(x, y, z, qx, qy, qz, qw)
            if result:
                rospy.loginfo("Goal execution done!")
    except rospy.ROSInterruptException:
        rospy.loginfo("Navigation test finished.")

