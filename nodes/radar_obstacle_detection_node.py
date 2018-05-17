#!/usr/bin/env python

import rospy
from marine_msgs.msg import RadarSectorStamped
from std_msgs.msg import Float32

radar_buffer = {}
range_m = 0.0
obstacle_publisher = None

short_range_cutoff = 25 # distance where short range ends
short_range_angle = 20 # angle to look for obstacles between 0 and short_range_cutoff
long_range_angle = 10 # angle to look for obstacles beyond short_range_cutoff

short_range_angle_range = (360-(short_range_angle/2),short_range_angle/2)
long_range_angle_range = (360-(long_range_angle/2),long_range_angle/2)

def radar_callback(data):
    global radar_buffer
    global range_m
    for s in data.sector.scanlines:
        if s.angle > short_range_angle_range[0] or s.angle < short_range_angle_range[1]:
            radar_buffer[s.angle] = s
            range_m = s.range
    if len(radar_buffer):
        avg_intensities = []
        for i in range(len(radar_buffer[radar_buffer.keys()[0]].intensities)):
            avg_intensities.append(0)
        #print radar_buffer
        bin_size =  range_m/float(len(avg_intensities))
        for s in radar_buffer.itervalues():
            for i in range(4,len(s.intensities)):
                if i*bin_size > short_range_cutoff and (s.angle > long_range_angle_range[0] or s.angle < long_range_angle_range[1]):
                    avg_intensities[i] += (ord(s.intensities[i])/255.0)/float(len(radar_buffer))*short_range_angle/long_range_angle                                        
                else:
                    avg_intensities[i] += (ord(s.intensities[i])/255.0)/float(len(radar_buffer))
        #print range_m, range_m/float(len(avg_intensities)) ,  avg_intensities[0:50]
        nearest = None
        for i in range(len(avg_intensities)):
            if avg_intensities[i] > .15:
                nearest = i*bin_size
                break
        #print 'nearest:',nearest
        f32 = Float32()
        if nearest is None:
            f32.data = -1
        else:
            f32.data = nearest
        obstacle_publisher.publish(f32)


    

if __name__ == '__main__':
    rospy.init_node('radar_obstacle_detection', anonymous=False)
    rospy.Subscriber('/radar', RadarSectorStamped, radar_callback)
    obstacle_publisher = rospy.Publisher('/obstacle_distance', Float32, queue_size=10)
    rospy.spin()


