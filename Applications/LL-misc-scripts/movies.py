# -*- coding: utf-8 -*-
"""
Created on Sat Oct 22 12:10:05 2016

@author: laughreyl
"""

import os

import cv2
import numpy as np


def showimg(title, img):
        img_nparry = np.asarray(img )
        cv2.imshow(title,img_nparry)
        cv2.waitKey()
        

        
movie_name = 'c:\\Users\\labadmin\\Documents\\GitHub\\LL-DAM-Analysis\\fly_movie.avi'
print("movie name = ", movie_name)
print('file exists? ',os.path.isfile(movie_name))

capture = cv2.VideoCapture(movie_name)
for k in range(0,20):
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

# for framenum in range(0, int(frame_count)):
#     success,frame_nparry = capture.read()
#     print(framenum,'frame type = ',type(frame_nparry))
#     frame_cvmat = cv2.cv.fromarray(frame_nparry)
#     print(framenum,'frame type = ',type(frame_cvmat))
#
#
#     #%%                                         numpy array functions
#
#     showimg('nparry title', frame_nparry)
#
#     cv2.GaussianBlur((frame_nparry), (3, 3), 0)                                      # what do the numbers mean?
#
#     im_bw = cv2.threshold(frame_nparry, 20, 255, cv2.THRESH_BINARY)[1]
# #    th, dst = cv2.threshold(temp, 20, 255, cv2.THRESH_BINARY)
#
#     framecopy_nparry = frame_nparry.copy()              #  THIS WORKS!
#
#     print(frame_nparry.shape)
#
# #    grey_image_nparry = cv2.cv.CreateImage(cv2.cv.GetSize(frame_nparry), cv2.cv.IPL_DEPTH_32F, 3)  # TypeError: CvArr argument 'arr' must be IplImage, CvMat or CvMatND. Use fromarray() to convert numpy arrays to CvMat or cvMatND
#
# #    cv2.imshow(frame_nparry)    #  TypeError: Required argument 'mat' (pos 2) not found
#
# #    cv2.cv.ConvertScale(frame_nparry, moving_average_nparry, 1.0, 0.0)              # TypeError: CvArr argument 'src' must be IplImage, CvMat or CvMatND. Use fromarray() to convert numpy arrays to CvMat or cvMatND
#
#
# #%%                                         cv2.cv.cvmat array functions
#
#     showimg('cvmat title', frame_cvmat)
#
#
#     print(frame_cvmat)
#     cv.cvarrToMat(frame_cvmat)
#     cv2.cv.imshow('window name',frame_cvmat)
#     cv2.waitKey()
#
#     print('frame_cvmat = ',type(frame_cvmat),cv2.cv.GetSize(frame_cvmat),
#               np.asarray(frame_cvmat[:,:,:]).shape)
#
#     framecopy_cvmat = copy.copy(frame_cvmat)    # THIS WORKS if you import copy!
# #    framecopy_cvmat = frame_cvmat.copy()            # AttributeError: 'cv2.cv.cvmat' object has no attribute 'copy'
# #    framecopy_cvmat = cv2.cv.clone(frame_cvmat)  # 'module' object has no attribute 'clone'
# #    framecopy_cvmat = frame_cvmat.clone()
#
#     tuple(frame_cvmat.shape[1::-1])
#
#     h, w = cv2.cv.GetSize(frame_cvmat)
#     grey_image_cvmat = cv2.cv.CreateMat(h, w, cv2.cv.CV_8UC1)
#     grey_image_cvmat = cv2.cv.CreateImage(cv2.cv.GetSize(frame_cvmat), cv2.cv.IPL_DEPTH_8U, 1)
#
#
#     moving_average_cvmat = cv2.cv.CreateImage(cv2.cv.GetSize(frame_cvmat), cv2.cv.IPL_DEPTH_32F, 3)
#     cv2.cv.ConvertScale(frame_cvmat, moving_average_cvmat, 1.0, 0.0)
#
#     cv2.cv.RunningAvg(frame_cvmat, moving_average_cvmat, 0.2, None)           #0.04
# #    cv2.accumulateWeighted(frame_cvmat, moving_average_cvmat, 0.2, None)           #TypeError: src is not a numpy array, neither a scalar
#
#
#
#
#     cv2.cv.AbsDiff(frame_cvmat, temp_cvmat, difference_cvmat)
#
# #    cv2.imshow(frame_cvmat)    #TypeError: Required argument 'mat' (pos 2) not found
#

#%%
#   raw_input('press enter to continue')
# cv2.getGaussianKernel()

capture.release()

