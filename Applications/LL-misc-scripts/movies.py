# -*- coding: utf-8 -*-
"""
Created on Sat Oct 22 12:10:05 2016

@author: laughreyl
"""

import cv2, cv, os
import numpy as np
import copy
    
def showimg(title, img):
        img_nparry = np.asarray(img )
        cv2.imshow(title,img_nparry)
        cv2.waitKey()
        

movie_name = 'F:\\Videos\\bias_video_cam_0_date_2016_07_27_time_16_04_13_v001.avi'
print("movie name = ", movie_name)
print('file exists? %s',os.path.isfile(movie_name))

capture = cv2.VideoCapture(movie_name)
for k in range(0,10):
    if not capture.isOpened():
        capture = cv2.VideoCapture(movie_name)
        cv2.waitKey(1000)
        print "Wait for the header"


if( capture.isOpened() ):
    print(' opened' )
else : print('not opened')

frame_width = capture.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)        # Width of the frames in the video stream.
frame_height = capture.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)       # Height of the frames in the video stream.
frame_rate = capture.get(cv2.cv.CV_CAP_PROP_FPS)                   # Frame rate.
frame_count = capture.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT)          # Number of frames in the video file.

print(frame_width, frame_height, frame_rate, frame_count)


capture.release()

