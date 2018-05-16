#!/usr/bin/env python

import rospy
from marine_msgs.msg import RadarSector

radar_buffer = {}

def radar_callback(data):
    global radar_buffer
    for s in data.scanlines:
        if s.angle > 355 or s.angle < 5:
	    #print s.angle, s.range,
            #for i in range(2,100):
            #    print ord(s.intensities[i]),
            #print
            radar_buffer[s.angle] = s
    if len(radar_buffer):
        avg_intensities = []
        for i in range(len(radar_buffer[radar_buffer.keys()[0]].intensities)):
            avg_intensities.append(0)
        #print radar_buffer
        for s in radar_buffer.itervalues():
            for i in range(2,len(s.intensities)):
                avg_intensities[i] += (ord(s.intensities[i])/255.0)/float(len(radar_buffer))
        print avg_intensities[0:0]


    

if __name__ == '__main__':
    rospy.init_node('radar_obstacle_detection', anonymous=False)
    rospy.Subscriber('/radar', RadarSector, radar_callback)
    rospy.spin()


