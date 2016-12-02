# -*- coding: utf-8 -*-
"""
Created on Sat Oct 01 22:54:37 2016

@author: laughreyl
"""

monitor1 = 'C:\\Users\\laughreyl\\Documents\\DAM_Analysis\\Data\\__20160823-135217__\\bias_video_cam_0_date_2016_08_23_time_13_52_17_v001.avi'

dateindex = monitor1.find("date_")
date = monitor1[dateindex+5:dateindex+15]
print(date)

timeindex = monitor1.find("time_")
time = monitor1[timeindex+5:timeindex+13]
print(time)

