# -*- coding: utf-8 -*-
#
#       pvg.py pysolovideogui
#
#
#       Copyright 2011 Giorgio Gilestro <giorgio@gilest.ro>
#
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.
#
#
"""Version 1.0

Interaction with webcam:                opencv      liveShow.py / imageAquisition.py
Saving movies as stream:                opencv      realCam
Saving movies as single files:          ?           realCam
Opening movies as avi:                  opencv      virtualCamMovie
Opening movies as sequence of files:    PIL         virtualCamFrames

Each Monitor has a camera that can be: realCam || VirtualCamMovies || VirtualCamFrames
The class monitor is handling the motion detection and data processing while the CAM only handle
IO of image sources

Algorithm for motion analysis:          PIL through kmeans (vector quantization)
    http://en.wikipedia.org/wiki/Vector_quantization
    http://stackoverflow.com/questions/3923906/kmeans-in-opencv-python-interface
"""

"""
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%  Imports
"""
from inspect import currentframe  # debug
from db import debugprt
import cv2, cv
import cPickle
import os, sys, datetime
import numpy as np

"""
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%   Settings
"""
pgm = 'pysolovideo.py'
call_tracking = False  # if True each function will report it's beginning and end
show_imgs = False  # if true, show images

""" %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Datetime settings  """
real_dt = datetime.datetime(2016, 11, 17, 17, 51, 38)  # start datetime of movie
delta_dt = 60  # write a row every minute

t = datetime.time(19, 1, 00)  # get datetime for adjusting from 31 Dec 1969 at 19:01:00
d = datetime.date(1969, 12, 31)
zero_dt = datetime.datetime.combine(d, t)
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

# get root dir name for all file operations
#
import ctypes.wintypes

CSIDL_PERSONAL = 5  # My Documents
SHGFP_TYPE_CURRENT = 0  # Get current, not default value
buf = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)  # get user document folder path
ctypes.windll.shell32.SHGetFolderPathW(None, CSIDL_PERSONAL, None, SHGFP_TYPE_CURRENT, buf)
root_dir = buf.value + '\\GitHub\\LL-DAM-Analysis\\'
data_dir = root_dir + 'Data\\Working_files\\'

DEFAULT_CONFIG = 'pysolo_video.cfg'

pySoloVideoVersion = 'dev'
MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']


def getCameraCount():
    if call_tracking:  debugprt(currentframe(), pgm, 'begin          ')
    """
    FIX THIS
    """
    n = 0
    Cameras = True

    while Cameras:
        try:
            print (cv.CaptureFromCAM(n))
            n += 1
        except:
            Cameras = False
    if call_tracking:  debugprt(self, currentframe(), pgm, 'end   ')
    return n


class Cam:
    """
    Functions and properties inherited by all cams
    """

    def __addText__(self, frame, text=None):
        if call_tracking:  debugprt(self, currentframe(), pgm, 'begin     ')  # debug
        """
        Add current time as stamp to the image
        """

        if not text: text = time.asctime(time.localtime(time.time()))

        normalfont = cv.InitFont(cv.CV_FONT_HERSHEY_PLAIN, 1, 1, 0, 1, 8)
        boldfont = cv.InitFont(cv.CV_FONT_HERSHEY_SIMPLEX, 1, 1, 0, 3, 8)
        font = normalfont
        textcolor = (255, 255, 255)

        (x1, _), ymin = cv.GetTextSize(text, font)
        width, height = frame.width, frame.height
        x = width - x1 - (width / 64)
        y = height - ymin - 2

        cv.PutText(frame, text, (x, y), font, textcolor)

        if call_tracking:  debugprt(self, currentframe(), pgm, 'end   ')
        return frame

    def getResolution(self):
        if call_tracking:  debugprt(self, currentframe(), pgm, 'begin     ')  # debug
        """
        Returns frame resolution as tuple (w,h)
        """
        a = self.resolution
        if call_tracking:  debugprt(self, currentframe(), pgm, 'end   ')
        return a

    def saveSnapshot(self, filename, quality=90, timestamp=False):
        if call_tracking:  debugprt(self, currentframe(), pgm, 'begin     ')  # debug
        """
        """
        img = self.getImage(timestamp, imgType)
        cv.SaveImage(filename, img)  # with opencv
        if call_tracking:  debugprt(self, currentframe(), pgm, 'end   ')

    def close(self):
        if call_tracking:  debugprt(self, currentframe(), pgm, 'begin     ')  # debug
        """
        """
        pass
        if call_tracking:  debugprt(self, currentframe(), pgm, 'end   ')


class realCam(Cam):
    """
    a realCam class will handle a webcam connected to the system
    camera is handled through opencv and images can be transformed to PIL
    """

    def __init__(self, devnum=0, resolution=(640, 480)):
        if call_tracking:  debugprt(self, currentframe(), pgm, 'begin     ')  # debug

        self.devnum = devnum
        self.resolution = resolution
        self.scale = False

        self.__initCamera()
        if call_tracking:  debugprt(self, currentframe(), pgm, 'end   ')

    def __initCamera(self):
        if call_tracking:  debugprt(self, currentframe(), pgm, 'begin     ')  # debug
        """
        """
        self.camera = cv.CaptureFromCAM(self.devnum)
        self.setResolution(self.resolution)
        if call_tracking:  debugprt(self, currentframe(), pgm, 'end   ')

    def getFrameTime(self):
        if call_tracking: debugprt(self, currentframe(), pgm, 'begin     ')  # debug
        """
        """
        a = time.time()  # current time epoch in secs.ms
        if call_tracking:  debugprt(self, currentframe(), pgm, 'end   ')
        return a

    def addTimeStamp(self, img):
        if call_tracking:  debugprt(self, currentframe(), pgm, 'begin     ')  # debug
        """
        """
        a = self.__addText__(img)
        if call_tracking:  debugprt(self, currentframe(), pgm, 'end   ')
        return a

    def setResolution(self, (x, y)):
        if call_tracking:  debugprt(self, currentframe(), pgm, 'begin     ')  # debug
        """
        Set resolution of the camera we are acquiring from
        """
        x = int(x);
        y = int(y)
        self.resolution = (x, y)
        cv.SetCaptureProperty(self.camera, cv.CV_CAP_PROP_FRAME_WIDTH, x)
        cv.SetCaptureProperty(self.camera, cv.CV_CAP_PROP_FRAME_HEIGHT, y)
        x1, y1 = self.getResolution()
        self.scale = ((x, y) != (x1, y1))  # if the camera does not support resolution, we need to scale the image
        if call_tracking:  debugprt(self, currentframe(), pgm, 'end   ')

    def getResolution(self):
        if call_tracking:  debugprt(self, currentframe(), pgm, 'begin     ')  # debug
        """
        Return real resolution
        """
        x1 = cv.GetCaptureProperty(self.camera, cv.CV_CAP_PROP_FRAME_WIDTH)
        y1 = cv.GetCaptureProperty(self.camera, cv.CV_CAP_PROP_FRAME_HEIGHT)
        a = (int(x1), int(y1))
        if call_tracking:  debugprt(self, currentframe(), pgm, 'end   ')
        return a

    def getImage(self, timestamp=False):
        if call_tracking: debugprt(self, currentframe(), pgm, 'begin     ')  # debug
        """
        class realcam
        Returns frame

        timestamp   False   (Default) Does not add timestamp
                    True              Add timestamp to the image

        """
        # frame = None

        if not self.camera:
            self.__initCamera()

        frame = cv.QueryFrame(self.camera)

        if self.scale:
            newsize = cv.CreateImage(self.resolution, cv.IPL_DEPTH_8U, 3)
            if type(frame) != type(newsize):
                if call_tracking:  debugprt(self, currentframe(), pgm, 'end   ')
                return newsize
            cv.Resize(frame, newsize)
            frame = newsize

        if timestamp: frame = self.__addText__(frame)

        if call_tracking:  debugprt(self, currentframe(), pgm, 'end   ')
        return frame

    def isLastFrame(self):
        if call_tracking:  debugprt(self, currentframe(), pgm, 'begin     ')  # debug
        """
        Added for compatibility with other cams
        """
        if call_tracking:  debugprt(self, currentframe(), pgm, 'end   ')
        return False

    def close(self):
        if call_tracking:  debugprt(self, currentframe(), pgm, 'begin     ')  # debug
        """
        Closes the connection
        """
        print "attempting to close stream"

        del (self.camera)  # cv.ReleaseCapture(self.camera)
        self.camera = None
        if call_tracking:  debugprt(self, currentframe(), pgm, 'end   ')


class virtualCamMovie(Cam):
    """
    A Virtual cam to be used to pick images from a movie (avi, mov) rather than a real webcam
    Images are handled through opencv
    """

    def __init__(self, path, step=None, start=None, end=None, loop=False, resolution=None):
        if call_tracking:  debugprt(self, currentframe(), pgm, 'begin     ')  # debug
        """
        Specifies some of the parameters for working with the movie:

            path        the path to the file

            step        distance between frames. If None, set 1

            start       start at frame. If None, starts at first

            end         end at frame. If None, ends at last

            loop        False   (Default)   Does not playback movie in a loop
                        True                Playback in a loop

        """
        self.path = path

        if start < 0: start = 0
        self.start = start or 0
        self.currentFrame = self.start

        self.step = step or 1
        if self.step < 1: self.step = 1

        self.loop = loop

        print('$$$$$$ pysolovideo, virtualcammovie, init  will capture file: ', self.path)
        self.capture = cv.CaptureFromFile(self.path)

        # finding the input resolution
        w = cv.GetCaptureProperty(self.capture, cv.CV_CAP_PROP_FRAME_WIDTH)
        h = cv.GetCaptureProperty(self.capture, cv.CV_CAP_PROP_FRAME_HEIGHT)
        self.in_resolution = (int(w), int(h))
        self.resolution = self.in_resolution

        # setting the output resolution
        self.setResolution(*resolution)

        self.totalFrames = self.getTotalFrames()
        if end < 1 or end > self.totalFrames: end = self.totalFrames
        self.lastFrame = end

        self.blackFrame = cv.CreateImage(self.resolution, cv.IPL_DEPTH_8U, 3)
        cv.Zero(self.blackFrame)
        if call_tracking:  debugprt(self, currentframe(), pgm, 'end   ')

    def getFrameTime(self, asString=None):
        if call_tracking: debugprt(self, currentframe(), pgm, 'begin     ')  # debug
        """
        Return the time of the frame
        """

        frameTime = cv.GetCaptureProperty(self.capture, cv.CV_CAP_PROP_POS_MSEC)

        # # print('$$$$$$, pysolovideo, getframetime, 326, will return 1/1000th of frametime = ,',frameTime)
        if asString:
            frameTime = str(datetime.timedelta(seconds=frameTime / 100.0))
            if call_tracking:  debugprt(self, currentframe(), pgm, 'end   ')
            return '%s - %s/%s' % (frameTime, self.currentFrame,
                                   self.totalFrames)  # was time.asctime(time.localtime(fileTime))  -> why do we care what the current time is?
        else:
            if call_tracking:  debugprt(self, currentframe(), pgm, 'end   ')
            return frameTime / 1000.0  # returning seconds compatibility reasons

    def getImage(self, timestamp=False):
        if call_tracking: debugprt(self, currentframe(), pgm, 'begin     ')  # debug
        """
        class virtualcammovie
        Returns frame

        timestamp   False   (Default) Does not add timestamp
                    True              Add timestamp to the image

        """

        # cv.SetCaptureProperty(self.capture, cv.CV_CAP_PROP_POS_FRAMES, self.currentFrame)
        # this does not work properly. Image is very corrupted
        im = cv.QueryFrame(self.capture)

        self.currentFrame += self.step
        print('$$$$$$ current frame =', self.currentFrame)

        if not im:
            im = self.blackFrame
            sysout = sys.__stdout__

            print('$$$$$$, pysolovideo, getImage, 353, cv.QueryFrame = false')
            return False                                                                    ## LL - added



        elif ((self.currentFrame > self.lastFrame) and (not self.loop)):
            sysout = sys.__stdout__
            print('$$$$$$, pysolovideo, getImage, 361, currentFrame > lastFrame')


            return False

        if self.scale:
            newsize = cv.CreateImage(self.resolution, cv.IPL_DEPTH_8U, 3)
            cv.Resize(im, newsize)
            im = newsize
            # # print('$$$$$$, pysolovideo, getImage, 371, image resized')

        if timestamp:
            text = self.getFrameTime(asString=True)
            im = self.__addText__(im, text)

        if call_tracking: debugprt(self, currentframe(), pgm, 'end   ')
        return im

    def setResolution(self, w, h):
        if call_tracking:  debugprt(self, currentframe(), pgm, 'begin     ')  # debug
        """
        Changes the output resolution
        """
        self.resolution = (w, h)
        self.scale = (self.resolution != self.in_resolution)
        if call_tracking:  debugprt(self, currentframe(), pgm, 'end   ')

    def getTotalFrames(self):
        if call_tracking:  debugprt(self, currentframe(), pgm, 'begin     ')  # debug
        """
        Returns total number of frames
        Be aware of this bug
        https://code.ros.org/trac/opencv/ticket/851
        """
        a = cv.GetCaptureProperty(self.capture, cv.CV_CAP_PROP_FRAME_COUNT)

        print('$$$$$$, pysolovideo, getImage, 398, total frames = ,', a)

        if call_tracking:  debugprt(self, currentframe(), pgm, 'end   ')
        return a

    def isLastFrame(self):
        if call_tracking:  debugprt(self, currentframe(), pgm, 'begin     ')  # debug
        """
        Are we processing the last frame in the movie?
        """

        if (self.currentFrame >= self.totalFrames) and not self.loop:
            if call_tracking:  debugprt(self, currentframe(), pgm, 'end   ')
            return True
        elif (self.currentFrame >= self.totalFrames) and self.loop:
            self.currentFrame = self.start
            if call_tracking:  debugprt(self, currentframe(), pgm, 'end   ')
            return False
        else:
            if call_tracking:  debugprt(self, currentframe(), pgm, 'end   ')
            return False


class virtualCamFrames(Cam):
    """
    A Virtual cam to be used to pick images from a folder rather than a webcam
    Images are handled through PIL
    """

    def __init__(self, path, resolution=None, step=None, start=None, end=None, loop=False):
        if call_tracking:  debugprt(self, currentframe(), pgm, 'begin     ')  # debug
        self.path = path
        self.fileList = self.__populateList__(start, end, step)
        self.totalFrames = len(self.fileList)

        self.currentFrame = 0
        self.last_time = None
        self.loop = False

        fp = os.path.join(self.path, self.fileList[0])

        self.in_resolution = cv.GetSize(cv.LoadImage(fp))
        if not resolution: resolution = self.in_resolution
        self.resolution = resolution
        self.scale = (self.in_resolution != self.resolution)
        if call_tracking:  debugprt(self, currentframe(), pgm, 'end   ')

    def getFrameTime(self, asString=None):
        if call_tracking: debugprt(self, currentframe(), pgm, 'begin     ')  # debug
        """
        Return the time of most recent content modification of the file fname
        """
        n = self.currentFrame
        fname = os.path.join(self.path, self.fileList[n])

        manual = False
        if manual:
            if call_tracking:  debugprt(self, currentframe(), pgm, 'end   ')
            # print('$$$$$$, pysolovideo, getframetime, 454, returns currentFrame')
            return self.currentFrame

        if fname and asString:
            fileTime = os.stat(fname)[-2]
            a = time.asctime(time.localtime(fileTime))
            # print('$$$$$$, pysolovideo, getframetime, 460, most recent modification time = ,',a)
            if call_tracking:  debugprt(self, currentframe(), pgm, 'end   ')
            return a
        elif fname and not asString:
            fileTime = os.stat(fname)[-2]
            # print('$$$$$$, pysolovideo, getframetime, 465, most recent modification time = ,',fileTime)
            if call_tracking:  debugprt(self, currentframe(), pgm, 'end   ')
            return fileTime

    def __populateList__(self, start, end, step):
        if call_tracking:  debugprt(self, currentframe(), pgm, 'begin     ')  # debug
        """
        Populate the file list
        """

        fileList = []
        fileListTmp = os.listdir(self.path)

        for fileName in fileListTmp:
            if '.tif' in fileName or '.jpg' in fileName:
                fileList.append(fileName)

        fileList.sort()
        a = fileList[start:end:step]
        if call_tracking:  debugprt(self, currentframe(), pgm, 'end   ')
        return a

    def getImage(self, timestamp=False):
        if call_tracking: debugprt(self, currentframe(), pgm, 'begin     ')  # debug
        """
        class virtualCamFrames
        Returns frame

        timestamp   False   (Default) Does not add timestamp
                    True              Add timestamp to the image
        """
        n = self.currentFrame
        fp = os.path.join(self.path, self.fileList[n])

        self.currentFrame += 1

        try:
            im = cv.LoadImage(fp)  # using cv to open the file

        except:
            print ('error with image %s' % fp)
            raise

        if self.scale:
            newsize = cv.CreateMat(self.resolution[0], self.resolution[1], cv.CV_8UC3)
            cv.Resize(im, newsize)

        self.last_time = self.getFrameTime(asString=True)

        if timestamp:
            im = self.__addText__(im, self.last_time)

        if call_tracking: debugprt(self, currentframe(), pgm, 'end   ')
        return im

    def getTotalFrames(self):
        if call_tracking:  debugprt(self, currentframe(), pgm, 'begin     ')  # debug
        """
        Return the total number of frames
        """
        if call_tracking:  debugprt(self, currentframe(), pgm, 'end   ')
        return self.totalFrames

    def isLastFrame(self):
        if call_tracking:  debugprt(self, currentframe(), pgm, 'begin     ')  # debug
        """
        Are we processing the last frame in the folder?
        """

        if (self.currentFrame == self.totalFrames) and not self.loop:
            if call_tracking:  debugprt(self, currentframe(), pgm, 'end   ')
            return True
        elif (self.currentFrame == self.totalFrames) and self.loop:
            self.currentFrame = 0
            if call_tracking:  debugprt(self, currentframe(), pgm, 'end   ')
            return False
        else:
            if call_tracking:  debugprt(self, currentframe(), pgm, 'end   ')
            return False

    def setResolution(self, w, h):
        if call_tracking:  debugprt(self, currentframe(), pgm, 'begin     ')  # debug
        """
        Changes the output resolution
        """
        self.resolution = (w, h)
        self.scale = (self.resolution != self.in_resolution)
        if call_tracking:  debugprt(self, currentframe(), pgm, 'end   ')

    def compressAllImages(self, compression=90, resolution=(960, 720)):
        if call_tracking:  debugprt(self, currentframe(), pgm, 'begin     ')  # debug
        """
        FIX THIS: is this needed?
        Load all images one by one and save them in a new folder
        """
        x, y = resolution[0], resolution[1]
        if self.isVirtualCam:
            in_path = self.cam.path
            out_path = os.path.join(in_path, 'compressed_%sx%s_%02d' % (x, y, compression))
            os.mkdir(out_path)

            for img in self.cam.fileList:
                f_in = os.path.join(in_path, img)
                im = Image.open(f_in)
                if im.size != resolution:
                    im = im.resize(resolution, Image.ANTIALIAS)

                f_out = os.path.join(out_path, img)
                im.save(f_out, quality=compression)

            if call_tracking:  debugprt(self, currentframe(), pgm, 'end   ')
            return True

        else:
            if call_tracking:  debugprt(self, currentframe(), pgm, 'end   ')
            return False


class Arena():
    """
    The arena define the space where the flies move
    Carries information about the ROI (coordinates defining each vial) and
    the number of flies in each vial

    The class monitor takes care of the camera
    The class arena takes care of the flies
    """

    def __init__(self, parent):
        if call_tracking:  debugprt(self, currentframe(), pgm, 'begin     ')  # debug

        self.monitor = parent

        self.ROIS = []  # Regions of interest
        self.beams = []  # beams: absolute coordinates
        self.trackType = 1
        self.ROAS = []  # Regions of Action
        self.minuteFPS = []

        self.period = 31  # in frames                # account for indexing differences btw python & people (2-> 1 frame at a time; 61-> 60 frames per period)
        self.ratio = 0
        self.rowline = 0

        self.points_to_track = []

        # (-1,-1)
        self.firstPosition = (0, 0)

        # shape ( self.period (x,y )
        self.__fa = np.zeros((self.period, 2), dtype=np.int)

        # shape ( flies, seconds, (x,y) ) Contains the coordinates of the last second (if fps > 1, average)
        self.flyDataBuffer = np.zeros((1, 2), dtype=np.int)

        # shape ( flies, self.period, (x,y) ) Contains the coordinates of the last minute (or period)
        self.flyDataMin = np.zeros((1, self.period, 2), dtype=np.int)

        self.count_seconds = 0
        self.__n = 0
        self.outputFile = None
        if call_tracking:  debugprt(self, currentframe(), pgm, 'end   ')

    def __relativeBeams(self):
        if call_tracking:  debugprt(self, currentframe(), pgm, 'begin     ')  # debug
        """
        Return the coordinates of the beam
        relative to the ROI to which they belong
        """

        newbeams = []

        for ROI, beam in zip(self.ROIS, self.beams):
            rx, ry = self.__ROItoRect(ROI)[0]
            (bx0, by0), (bx1, by1) = beam

            newbeams.append(((bx0 - rx, by0 - ry), (bx1 - rx, by1 - ry)))

        if call_tracking:  debugprt(self, currentframe(), pgm, 'end   ')
        return newbeams

    def __ROItoRect(self, coords):
        if call_tracking:  debugprt(self, currentframe(), pgm, 'begin     ')  # debug
        """
        Used internally
        Converts a ROI (a tuple of four points coordinates) into
        a Rect (a tuple of two points coordinates)
        """
        (x1, y1), (x2, y2), (x3, y3), (x4, y4) = coords
        lx = min([x1, x2, x3, x4])
        rx = max([x1, x2, x3, x4])
        uy = min([y1, y2, y3, y4])
        ly = max([y1, y2, y3, y4])

        if call_tracking:  debugprt(self, currentframe(), pgm, 'end   ')
        return ((lx, uy), (rx, ly))

    def __distance(self, (x1, y1), (x2, y2)):
        if call_tracking:  debugprt(self, currentframe(), pgm, 'begin     ')  # debug
        """
        Calculate the distance between two cartesian points
        """
        if call_tracking:  debugprt(self, currentframe(), pgm, 'end   ')
        return np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    def __getMidline(self, coords):
        if call_tracking:  debugprt(self, currentframe(), pgm, 'begin     ')  # debug
        """
        Return the position of each ROI's midline
        Will automatically determine the orientation of the vial
        """
        (x1, y1), (x2, y2) = self.__ROItoRect(coords)

        horizontal = abs(x2 - x1) > abs(y2 - y1)

        if horizontal:
            xm = x1 + (x2 - x1) / 2
            if call_tracking:  debugprt(self, currentframe(), pgm, 'end   ')
            return (xm, y1), (xm, y2)
        else:
            ym = y1 + (y2 - y1) / 2
            if call_tracking:  debugprt(self, currentframe(), pgm, 'end   ')
            return (x1, ym), (x2, ym)

    def calibrate(self, p1, p2, cm=1):
        if call_tracking:  debugprt(self, currentframe(), pgm, 'begin     ')  # debug
        """
        The distance between p1 and p2 will be set to be X cm
        (default 1 cm)
        """
        cm = float(cm)
        dpx = self.__distance(p1, p2)

        self.ratio = dpx / cm

        if call_tracking:  debugprt(self, currentframe(), pgm, 'end   ')
        return self.ratio

    def pxToCm(self, distance_px):
        if call_tracking:  debugprt(self, currentframe(), pgm, 'begin     ')  # debug
        """
        Converts distance from pixels to cm
        """
        print('$$$$$$, pysolovideo, pxtocm, 707 ', distance_px / self.ratio)  # debug

        if self.ratio:
            if call_tracking:  debugprt(self, currentframe(), pgm, 'end   ')
            return distance_px / self.ratio
        else:
            print "You need to calibrate the mask first!"
            if call_tracking:  debugprt(self, currentframe(), pgm, 'end   ')
            return distance_px

    def addROI(self, coords, n_flies):
        if call_tracking:  debugprt(self, currentframe(), pgm, 'begin     ')  #
        """
        Add a new ROI to the arena
        """
        self.ROIS.append(coords)
        self.beams.append(self.__getMidline(coords))
        self.points_to_track.append(n_flies)

        # these increase by one on the fly axis
        self.flyDataBuffer = np.append(self.flyDataBuffer, [self.firstPosition], axis=0)  # ( flies, 1, (x,y) )
        self.flyDataMin = np.append(self.flyDataMin, [self.__fa.copy()], axis=0)  # ( flies, self.period, (x,y) )
        if call_tracking:  debugprt(self, currentframe(), pgm, 'end   ')

    def getROI(self, n):
        if call_tracking:  debugprt(self, currentframe(), pgm, 'begin     ')  # debug
        """
        Returns the coordinates of the nth crop area
        """
        if n > len(self.ROIS):
            coords = []
        else:
            coords = self.ROIS[n]
        if call_tracking:  debugprt(self, currentframe(), pgm, 'end   ')
        return coords

    def delROI(self, n):
        if call_tracking:  debugprt(self, currentframe(), pgm, 'begin     ')  # debug
        """
        removes the nth crop area from the list
        if n -1, remove all
        """
        if n >= 0:
            self.ROIS.pop(n)
            self.points_to_track.pop(n)

            self.flyDataBuffer = np.delete(self.flyDataBuffer, n, axis=0)
            self.flyDataMin = np.delete(self.flyDataMin, n, axis=0)

        elif n < 0:
            self.ROIS = []
        if call_tracking:  debugprt(self, currentframe(), pgm, 'end   ')

    def getROInumber(self):
        if call_tracking:  debugprt(self, currentframe(), pgm, 'begin     ')  # debug
        """
        Return the number of current active ROIS
        """
        if call_tracking:  debugprt(self, currentframe(), pgm, 'end   ')
        return len(self.ROIS)

    def saveROIS(self, filename):
        if call_tracking:  debugprt(self, currentframe(), pgm, 'begin     ')  # debug
        """
        Save the current crop data to a file
        """
        cf = open(filename, 'w')
        cPickle.dump(self.ROIS, cf)
        cPickle.dump(self.points_to_track, cf)

        cf.close()
        if call_tracking:  debugprt(self, currentframe(), pgm, 'end   ')

    def loadROIS(self, filename):
        if call_tracking:  debugprt(self, currentframe(), pgm, 'begin     ')  # debug
        """
        Load the crop data from a file
        """
        try:
            cf = open(filename, 'r')
            self.ROIS = cPickle.load(cf)
            self.points_to_track = cPickle.load(cf)
            cf.close()

            f = len(self.ROIS)
            self.flyDataBuffer = np.zeros((f, 2), dtype=np.int)
            self.flyDataMin = np.zeros((f, self.period, 2), dtype=np.int)

            for coords in self.ROIS:
                self.beams.append(self.__getMidline(coords))

            if call_tracking:  debugprt(self, currentframe(), pgm, 'end   ')
            return True
        except:
            if call_tracking:  debugprt(self, currentframe(), pgm, 'end   ')
            return False

    def resizeROIS(self, origSize, newSize):
        if call_tracking:  debugprt(self, currentframe(), pgm, 'begin     ')  # debug
        """
        Resize the mask to new size so that it would properly fit
        resized images
        """
        newROIS = []

        ox, oy = origSize
        nx, ny = newSize
        xp = float(ox) / nx
        yp = float(oy) / ny

        for ROI in self.ROIS:
            nROI = []
            for pt in ROI:
                nROI.append((pt[0] * xp, pt[1] * yp))
            newROIS.append(ROI)

        if call_tracking:  debugprt(self, currentframe(), pgm, 'end   ')
        return newROIS

    def point_in_poly(self, pt, poly):
        if call_tracking:  debugprt(self, currentframe(), pgm, 'begin     ')  # debug
        """
        Determine if a point is inside a given polygon or not
        Polygon is a list of (x,y) pairs. This fuction
        returns True or False.  The algorithm is called
        "Ray Casting Method".
        polygon = [(x,y),(x1,x2),...,(x10,y10)]
        http://pseentertainmentcorp.com/smf/index.php?topic=545.0
        Alternatively:
        http://opencv.itseez.com/doc/tutorials/imgproc/shapedescriptors/point_polygon_test/point_polygon_test.html
        """
        x, y = pt

        n = len(poly)
        inside = False

        p1x, p1y = poly[0]
        for i in range(n + 1):
            p2x, p2y = poly[i % n]
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside
            p1x, p1y = p2x, p2y

        if call_tracking: debugprt(self, currentframe(), pgm, 'end   ')
        return inside

    def isPointInROI(self, pt):
        if call_tracking: debugprt(self, currentframe(), pgm, 'begin     ')  # debug
        """
        Check if a given point falls whithin one of the ROI
        Returns the ROI number or else returns -1
        """

        for ROI in self.ROIS:
            if self.point_in_poly(pt, ROI):
                return self.ROIS.index(ROI)

        if call_tracking: debugprt(self, currentframe(), pgm, 'end   ')
        return -1

    def ROIStoRect(self):
        if call_tracking: debugprt(self, currentframe(), pgm, 'begin     ')  # debug
        """
        translate ROI (list containing for points a tuples)
        into Rect (list containing two points as tuples)
        """
        newROIS = []
        for ROI in self.ROIS:
            newROIS.append(self.__ROItoRect(ROI))

        if call_tracking: debugprt(self, currentframe(), pgm, 'end   ')
        return newROIS

    def getLastSteps(self, fly, steps):
        if call_tracking: debugprt(self, currentframe(), pgm, 'begin     ')  # debug
        """
        """
        c = self.count_seconds
        a = [(x, y) for [x, y] in self.flyDataMin[fly][c - steps:c].tolist()] + [
            tuple(self.flyDataBuffer[fly].flatten())]
        if call_tracking: debugprt(self, currentframe(), pgm, 'end   ')
        return a

    def addFlyCoords(self, count, fly):
        if call_tracking: debugprt(self, currentframe(), pgm, 'begin     ')  # debug
        """
        Add the provided coordinates to the existing list
        count   int     the fly number in the arena
        fly     (x,y)   the coordinates to add
        Called for every fly moving in every frame
        """

        fly_size = 15  # About 15 pixels at 640x480
        max_movement = fly_size * 100
        min_movement = fly_size / 3

        previous_position = tuple(self.flyDataBuffer[count])
        isFirstMovement = (previous_position == self.firstPosition)
        fly = fly or previous_position  # Fly is None if no blob was detected

        distance = self.__distance(previous_position, fly)
        # print('$$$$$$, pysolovideo, addflycoords, 902, distance = ',distance,'  previous position = ',previous_position, '  fly = ',fly)
        if (distance > max_movement and not isFirstMovement) or (distance < min_movement):
            fly = previous_position

        # Does a running average for the coordinates of the fly at each frame to flyDataBuffer
        # This way the shape of flyDataBuffer is always (n, (x,y)) and once a second we just have to add the (x,y)
        # values to flyDataMin, whose shape is (n, 60, (x,y))
        self.flyDataBuffer[count] = np.append(self.flyDataBuffer[count], fly, axis=0).reshape(-1, 2).mean(axis=0)
        return fly, distance

    def compactSeconds(self, FPS, delta):
        if call_tracking:  debugprt(self, currentframe(), pgm, 'begin     ')  # debug
        """
        Compact the frames collected in the last second
        by averaging the value of the coordinates

        Called every second; flies treated at once
        FPS         current rate of frame per seconds
        delta       how much time has elapsed from the last "second"
        """
        self.minuteFPS.append(FPS)
        try: self.flyDataMin[:, self.__n] = self.flyDataBuffer
        except:
            sys.exit('Reached end of video ????   LL')


        if self.count_seconds + 1 >= self.period:
            self.writeActivity(fps=np.mean(self.minuteFPS))
            self.count_seconds = 0
            self.__n = 0
            self.minuteFPS = []

            for i in range(0, self.period):
                self.flyDataMin[:, i] = self.flyDataBuffer

        # growing continously; this is the correct thing to do but we would have problems adding new row with new ROIs
        # self.flyDataMin = np.append(self.flyDataMin, self.flyDataBuffer, axis=1)


        self.count_seconds += delta
        self.__n += 1
        if call_tracking:  debugprt(self, currentframe(), pgm, 'end   ')

    def writeActivity(self, fps=.5, extend=True):
        if call_tracking: debugprt(self, currentframe(), pgm, 'begin     ')  # debug
        """
        Write the activity to file
        Kind of motion depends on user settings

        Called every minute; flies treated at once
        1	09 Dec 11	19:02:19	1	0	1	0	0	0	?		[actual_activity]
        """
        global real_dt
        # Here we build the header
        # year, month, day, hh, mn, sec
        # movie_dt = datetime.datetime.fromtimestamp( self.monitor.getFrameTime() )    # NOT GETTING CORRECT date/time info
        # delta_dt = movie_dt - zero_dt
        # real_dt = start_dt +delta_dt
        real_dt = real_dt + datetime.timedelta(0, delta_dt)  # first real_dt and delta_dt are hard-coded in.  FIX THIS
        real_dt_str = real_dt.strftime('%d %b %y\t%H:%M:%S')

        # monitor is active
        active = '1'
        # average frames per seconds (FPS)
        damscan = int(round(fps))
        # tracktype
        tracktype = self.trackType
        # monitor with sleep deprivation capabilities?
        sleepDep = self.monitor.isSDMonitor * 1
        # monitor number, not yet implemented
        monitor = '0'
        # unused
        unused = 0
        # is light on or off?
        light = '0'  # changed to 0 from ? for compatability with SCAMP

        # : activity
        activity = []
        row = ''

        if self.trackType == 0:
            activity = [self.calculateDistances(), ]

        elif self.trackType == 1:
            activity = [self.calculateVBM(), ]

        elif self.trackType == 2:
            activity = self.calculatePosition()

        # print('$$$$$$ pysolovideo: writeactivity: 995:  activity = ,', activity)                                           # debug

        # Expand the readings to 32 flies for compatibility reasons with trikinetics
        flies = len(activity[0].split('\t'))
        if extend and flies < 32:
            extension = '\t' + '\t'.join(['0', ] * (32 - flies))
        else:
            extension = ''

        for line in activity:
            self.rowline += 1
            row_header = '%s\t' * 9 % (self.rowline, real_dt_str,
                                       active, damscan, tracktype, sleepDep,
                                       monitor, unused, light)
            row += row_header + line + extension + '\n'

        if self.outputFile:
            fh = open(self.outputFile, 'a')
            print('$$$$$$, pysolovideo, writeactivity, 1014,  row = ', row)  # debug
            fh.write(row)
            fh.close()

        if call_tracking:  debugprt(self, currentframe(), pgm, 'end   ')

    def calculateDistances(self):
        if call_tracking:  debugprt(self, currentframe(), pgm, 'begin     ')  # debug
        """
        Motion is calculated as distance in px per minutes
        """

        # shift by one second left flies, seconds, (x,y)
        fs = np.roll(self.flyDataMin, -1, axis=1)

        x = self.flyDataMin[:, :, :1]
        y = self.flyDataMin[:, :, 1:]

        x1 = fs[:, :, :1]
        y1 = fs[:, :, 1:]

        d = self.__distance((x, y), (x1, y1))
        # print('$$$$$$, pysolovideo, calcdists, 1021, x = ,', str(x[0]), ', y = ,', str(y[0]), ', x1 = ,', str(x1[0]),
        #       ', y1 = ,', str(y1[0]), 'd = ', str(d[0]))

        # we sum everything BUT the last bit of information otherwise we have data duplication
        values = d[:, :-1, :].sum(axis=1).reshape(-1)
        activity = '\t'.join(['%s' % int(v) for v in values])
        # print('$$$$$$, pysolovideo, writeactivity, calculatedistances, 1030, activity = ,', activity, ', values = ,',values)

        if call_tracking:  debugprt(self, currentframe(), pgm, 'end   ')
        return activity

    def calculateVBM(self):
        if call_tracking:  debugprt(self, currentframe(), pgm, 'begin     ')  # debug
        """
        Motion is calculated as virtual beam crossing
        Detects automatically beam orientation (vertical vs horizontal)
        """

        values = []

        for fd, md in zip(self.flyDataMin, self.__relativeBeams()):

            (mx1, my1), (mx2, my2) = md
            horizontal = (mx1 == mx2)

            fs = np.roll(fd, -1, 0)

            x = fd[:, :1];
            y = fd[:, 1:]  # THESE COORDINATES ARE RELATIVE TO THE ROI
            x1 = fs[:, :1];
            y1 = fs[:, 1:]

            if horizontal:
                crossed = (x < mx1) * (x1 > mx1) + (x > mx1) * (x1 < mx1)
            else:
                crossed = (y < my1) * (y1 > my1) + (y > my1) * (y1 < my1)

            values.append(crossed.sum())

        activity = '\t'.join([str(v) for v in values])
        if call_tracking:  debugprt(self, currentframe(), pgm, 'end   ')
        return activity

    def calculatePosition(self, resolution=1):
        if call_tracking:  debugprt(self, currentframe(), pgm, 'begin     ')  # debug
        """
        Simply write out position of the fly at every time interval, as
        decided by "resolution" (seconds)
        """

        activity = []
        rois = self.getROInumber()

        a = self.flyDataMin.transpose(1, 0, 2)  # ( interval, n_flies, (x,y) )
        a = a.reshape(resolution, -1, rois, 2).mean(0)

        for fd in a:
            onerow = '\t'.join(['%s,%s' % (x, y) for (x, y) in fd])
            activity.append(onerow)

        if call_tracking:  debugprt(self, currentframe(), pgm, 'end   ')
        return activity


class Monitor(object):
    """
    The main monitor class

    The class monitor takes care of the camera
    The class arena takes care of the flies
    """

    def __init__(self):
        if call_tracking:  debugprt(self, currentframe(), pgm, 'begin     ')  # debug
        """
        A Monitor contains a cam, which can be either virtual or real.
        Everything is handled through openCV
        """
        self.count = 0

        self.grabMovie = False
        self.writer = None
        self.cam = None

        self.arena = Arena(self)
        print('arena returned: ')
        print(self.arena)

        self.imageCount = 0
        self.lasttime = 0

        self.maxTick = 60

        self.__firstFrame = True
        self.tracking = True

        self.__tempFPS = 0
        self.processingFPS = 0

        self.drawPath = False
        self.isSDMonitor = False
        if call_tracking:  debugprt(self, currentframe(), pgm, 'end   ')

    def __drawBeam(self, img, bm, color=None):
        if call_tracking:  debugprt(self, currentframe(), pgm, 'begin     ')  # debug
        """
        Draw the Beam using given coordinates
        """
        if not color: color = (100, 100, 200)
        width = 1
        line_type = cv.CV_AA

        cv.Line(img, bm[0], bm[1], color, width, line_type, 0)

        if call_tracking:  debugprt(self, currentframe(), pgm, 'end   ')
        return img

    def __drawFPS(self, frame):
        if call_tracking:  debugprt(self, currentframe(), pgm, 'begin     ')  # debug
        """
        """

        normalfont = cv.InitFont(cv.CV_FONT_HERSHEY_PLAIN, 1, 1, 0, 1, 8)
        boldfont = cv.InitFont(cv.CV_FONT_HERSHEY_SIMPLEX, 1, 1, 0, 3, 8)
        font = normalfont
        textcolor = (255, 255, 255)
        text = "FPS: %02d" % self.processingFPS

        (x1, _), ymin = cv.GetTextSize(text, font)
        width, height = frame.width, frame.height
        x = (width / 64)
        y = height - ymin - 2

        cv.PutText(frame, text, (x, y), font, textcolor)

        if call_tracking:  debugprt(self, currentframe(), pgm, 'end   ')
        return frame

    def __drawROI(self, img, ROI, color=None, ROInum=None):
        if call_tracking:  debugprt(self, currentframe(), pgm, 'begin     ')  # debug
        """
        Draw ROI on img using given coordinates
        ROI is a tuple of 4 tuples ( (x1, y1), (x2, y2), (x3, y3), (x4, y4) )
        and does not have to be necessarily a rectangle
        """

        if not color: color = (255, 255, 255)
        width = 1
        line_type = cv.CV_AA

        cv.PolyLine(img, [ROI], is_closed=1, color=color, thickness=1, lineType=line_type, shift=0)

        if ROInum != None:
            x, y = ROI[0]
            font = cv.InitFont(cv.CV_FONT_HERSHEY_PLAIN, 1, 1, 0, 1, 8)
            textcolor = (255, 255, 255)
            text = "%02d" % ROInum
            cv.PutText(img, text, (x, y), font, textcolor)

        if call_tracking:  debugprt(self, currentframe(), pgm, 'end   ')
        return img

    def __drawCross(self, img, pt, color=None):
        if call_tracking:  debugprt(self, currentframe(), pgm, 'begin     ')  # debug
        """
        Draw a cross around a point pt
        """
        if not color: color = (255, 255, 255)
        width = 1
        line_type = cv.CV_AA

        x, y = pt
        a = (x, y - 5)
        b = (x, y + 5)
        c = (x - 5, y)
        d = (x + 5, y)

        cv.Line(img, a, b, color, width, line_type, 0)
        cv.Line(img, c, d, color, width, line_type, 0)

        if call_tracking:  debugprt(self, currentframe(), pgm, 'end   ')
        return img

    def __drawLastSteps(self, img, fly, steps=5, color=None):
        if call_tracking:  debugprt(self, currentframe(), pgm, 'begin     ')  # debug
        """
        Draw the last n (default 5) steps of the fly
        """

        if not color: color = (255, 255, 255)
        width = 1
        line_type = cv.CV_AA

        points = self.arena.getLastSteps(fly, steps)

        cv.PolyLine(img, [points], is_closed=0, color=color, thickness=1, lineType=line_type, shift=0)

        if call_tracking:  debugprt(self, currentframe(), pgm, 'end   ')
        return img

    def __getChannel(self, img, channel='R'):
        if call_tracking:  debugprt(self, currentframe(), pgm, 'begin     ')  # debug
        """
        Return only the asked channel R,G or B
        """

        cn = 'RGB'.find(channel.upper())

        channels = [None, None, None]
        cv.Split(img, channels[0], channels[1], channels[2], None)
        if call_tracking:  debugprt(self, currentframe(), pgm, 'end   ')
        return channels[cn]

    def __angle(self, pt1, pt2, pt0):
        if call_tracking:  debugprt(self, currentframe(), pgm, 'begin     ')  # debug
        """
        Return the angle between three points
        """
        dx1 = pt1[0] - pt0[0]
        dy1 = pt1[1] - pt0[1]
        dx2 = pt2[0] - pt0[0]
        dy2 = pt2[1] - pt0[1]
        if call_tracking:  debugprt(self, currentframe(), pgm, 'end   ')
        return (dx1 * dx2 + dy1 * dy2) / np.sqrt((dx1 * dx1 + dy1 * dy1) * (dx2 * dx2 + dy2 * dy2) + 1e-10)

    def close(self):
        if call_tracking:  debugprt(self, currentframe(), pgm, 'begin     ')  # debug
        """
        Closes stream
        """
        self.cam.close()
        if call_tracking:  debugprt(self, currentframe(), pgm, 'end   ')

    def CaptureFromCAM(self, devnum=0, resolution=(640, 480), options=None):
        if call_tracking:  debugprt(self, currentframe(), pgm, 'begin     ')  # debug
        """
        """
        self.isVirtualCam = False
        self.source = devnum

        self.resolution = resolution
        self.cam = realCam(devnum=devnum)
        self.cam.setResolution(resolution)
        self.resolution = self.cam.getResolution()
        self.numberOfFrames = 0
        if call_tracking:  debugprt(self, currentframe(), pgm, 'end   ')

    def CaptureFromMovie(self, camera, resolution=None, options=None):
        if call_tracking:  debugprt(self, currentframe(), pgm, 'begin     ')  # debug
        """
        """
        self.isVirtualCam = True
        self.source = camera

        if options:
            step = options['step']
            start = options['start']
            end = options['end']
            loop = options['loop']

        self.cam = virtualCamMovie(path=camera, resolution=resolution)
        self.resolution = self.cam.getResolution()
        self.numberOfFrames = self.cam.getTotalFrames()
        if call_tracking:  debugprt(self, currentframe(), pgm, 'end   ')

    def CaptureFromFrames(self, camera, resolution=None, options=None):
        if call_tracking:  debugprt(self, currentframe(), pgm, 'begin     ')  # debug
        """
        """
        self.isVirtualCam = True
        self.source = camera

        if options:
            step = options['step']
            start = options['start']
            end = options['end']
            loop = options['loop']

        self.cam = virtualCamFrames(path=camera, resolution=resolution)
        self.resolution = self.cam.getResolution()
        self.numberOfFrames = self.cam.getTotalFrames()
        if call_tracking:  debugprt(self, currentframe(), pgm, 'end   ')

    def hasSource(self):
        if call_tracking:  debugprt(self, currentframe(), pgm, 'begin     ')  # debug
        """
        """
        a = self.cam != None
        if call_tracking:  debugprt(self, currentframe(), pgm, 'end   ')
        return a

    def setSource(self, camera, resolution, options=None):
        if call_tracking:  debugprt(self, currentframe(), pgm, 'begin     ')  # debug
        """
        Set source intelligently
        """
        try:
            camera = int(camera)
        except:
            pass

        if type(camera) == type(0):
            self.CaptureFromCAM(camera, resolution, options)
        elif os.path.isfile(camera):
            self.CaptureFromMovie(camera, resolution, options)
        elif os.path.isdir(camera):
            self.CaptureFromFrames(camera, resolution, options)
        if call_tracking:  debugprt(self, currentframe(), pgm, 'end   ')

    def setTracking(self, track, trackType=0, mask_file='', outputFile=''):
        if call_tracking:  debugprt(self, currentframe(), pgm, 'begin     ')  # debug
        """
        Set the tracking parameters

        track       Boolean     Do we do tracking of flies?
        trackType   0           tracking using the virtual beam method
                    1 (Default) tracking calculating distance moved
        mask_file   text        the file used to load and store masks
        outputFile  text        the txt file where results will be saved
        """

        if trackType == None: trackType = 0
        if mask_file == None: mask_file = ''
        if outputFile == None: outputFile = ''

        self.track = track
        self.arena.trackType = int(trackType)
        self.mask_file = mask_file
        self.arena.outputFile = outputFile

        if mask_file:
            self.loadROIS(mask_file)
        if call_tracking:  debugprt(self, currentframe(), pgm, 'end   ')

    def getFrameTime(self):
        if call_tracking: debugprt(self, currentframe(), pgm, 'begin     ')  # debug
        """
        """
        a = self.cam.getFrameTime()
        if call_tracking:  debugprt(self, currentframe(), pgm, 'end   ')
        return a

    def isLastFrame(self):
        if call_tracking:  debugprt(self, currentframe(), pgm, 'begin     ')  # debug
        """
        Proxy to isLastFrame()
        Handled by camera
        """
        a = self.cam.isLastFrame()
        if call_tracking:  debugprt(self, currentframe(), pgm, 'end   ')
        return a

    def saveMovie(self, filename, fps=.5, codec='FMP4', startOnKey=False):     #  fps was 24
        if call_tracking:  debugprt(self, currentframe(), pgm, 'begin     ')  # debug
        """
        Determines whether all the frames grabbed through getImage will also
        be saved as movie.

        filename                           the full path to the file to be written
        fps             24   (Default)     number of frames per second
        codec           FMP4 (Default)     codec to be used

        http://stackoverflow.com/questions/5426637/writing-video-with-opencv-python-mac
        """
        fourcc = cv.CV_FOURCC(*[c for c in codec])

        self.writer = cv.CreateVideoWriter(filename, fourcc, fps, self.resolution, 1)
        self.grabMovie = not startOnKey
        if call_tracking:  debugprt(self, currentframe(), pgm, 'end   ')

    def saveSnapshot(self, *args, **kwargs):
        if call_tracking:  debugprt(self, currentframe(), pgm, 'begin     ')  # debug
        """
        proxy to saveSnapshot
        """
        self.cam.saveSnapshot(*args, **kwargs)
        if call_tracking:  debugprt(self, currentframe(), pgm, 'end   ')

    def SetLoop(self, loop):
        if call_tracking:  debugprt(self, currentframe(), pgm, 'begin     ')  # debug
        """
        Set Loop on or off.
        Will work only in virtual cam mode and not realCam
        Return current loopmode
        """
        if self.isVirtualCam:
            self.cam.loop = loop
            a = self.cam.loop
            if call_tracking:  debugprt(self, currentframe(), pgm, 'end   ')
            return a
        else:
            if call_tracking:  debugprt(self, currentframe(), pgm, 'end   ')
            return False

    def addROI(self, coords, n_flies=1):
        if call_tracking:  debugprt(self, currentframe(), pgm, 'begin     ')  # debug
        """
        Add the coords for a new ROI and the number of flies we want to track in that area
        selection       (pt1, pt2, pt3, pt4)    A four point selection
        n_flies         1    (Default)      Number of flies to be tracked in that area
        """

        self.arena.addROI(coords, n_flies)
        if call_tracking:  debugprt(self, currentframe(), pgm, 'end   ')

    def getROI(self, n):
        if call_tracking:  debugprt(self, currentframe(), pgm, 'begin     ')  # debug
        """
        Returns the coordinates of the nth crop area
        """
        a = self.arena.getROI(n)
        if call_tracking:  debugprt(self, currentframe(), pgm, 'end   ')
        return a

    def delROI(self, n):
        if call_tracking:  debugprt(self, currentframe(), pgm, 'begin     ')  # debug
        """
        removes the nth crop area from the list
        if n -1, remove all
        """
        self.arena.delROI(n)
        if call_tracking:  debugprt(self, currentframe(), pgm, 'end   ')

    def saveROIS(self, filename=None):
        if call_tracking:  debugprt(self, currentframe(), pgm, 'begin     ')  # debug
        """
        Save the current crop data to a file
        """
        if not filename: filename = self.mask_file
        self.arena.saveROIS(filename)
        if call_tracking:  debugprt(self, currentframe(), pgm, 'end   ')

    def loadROIS(self, filename=None):
        if call_tracking:  debugprt(self, currentframe(), pgm, 'begin     ')  # debug
        """
        Load the crop data from a file
        """
        if not filename: filename = self.mask_file
        a = self.arena.loadROIS(filename)
        if call_tracking:  debugprt(self, currentframe(), pgm, 'end   ')
        return a

    def resizeROIS(self, origSize, newSize):
        if call_tracking:  debugprt(self, currentframe(), pgm, 'begin     ')  # debug
        """
        Resize the mask to new size so that it would properly fit
        resized images
        """
        a = self.arena.resizeROIS(origSize, newSize)
        if call_tracking:  debugprt(self, currentframe(), pgm, 'end   ')
        return a

    def isPointInROI(self, pt):
        if call_tracking:  debugprt(self, currentframe(), pgm, 'begin     ')  # debug
        """
        Check if a given point falls whithin one of the ROI
        Returns the ROI number or else returns -1
        """
        a = self.arena.isPointInROI(pt)
        if call_tracking:  debugprt(self, currentframe(), pgm, 'end   ')
        return a

    def calibrate(self, pt1, pt2, cm=1):
        if call_tracking:  debugprt(self, currentframe(), pgm, 'begin     ')  # debug
        """
        Relays to arena calibrate
        """
        a = self.arena.calibrate(pt1, pt2, cm)
        if call_tracking:  debugprt(self, currentframe(), pgm, 'end   ')
        return a

    def autoMask(self, pt1, pt2):
        if call_tracking:  debugprt(self, currentframe(), pgm, 'begin     ')  # debug
        """
        EXPERIMENTAL, FIX THIS
        This is experimental
        For now it works only with one kind of arena
        Should be more flexible than this
        """
        rows = 16
        cols = 2
        food = .10
        vials = rows * cols
        ROI = [None, ] * vials

        (x, y), (x1, y1) = pt1, pt2
        w, h = (x1 - x), (y1 - y)

        d = h / rows
        l = (w / cols) - int(food / 2 * w)

        k = 0
        for v in range(rows):
            ROI[k] = (x, y), (x + l, y + d)
            ROI[k + 1] = (x1 - l, y), (x1, y + d)
            k += 2
            y += d

        nROI = []
        for R in ROI:
            (x, y), (x1, y1) = R
            self.arena.addROI(((x, y), (x, y1), (x1, y1), (x1, y)), 1)
        if call_tracking:  debugprt(self, currentframe(), pgm, 'end   ')

    def findOuterFrame(self, img, thresh=50):
        if call_tracking:  debugprt(self, currentframe(), pgm, 'begin     ')  # debug
        """
        EXPERIMENTAL
        Find the greater square
        """
        N = 11
        sz = (img.width & -2, img.height & -2)
        storage = cv.CreateMemStorage(0)
        timg = cv.CloneImage(img)
        gray = cv.CreateImage(sz, 8, 1)
        pyr = cv.CreateImage((img.width / 2, img.height / 2), 8, 3)

        squares = []
        # select the maximum ROI in the image
        # with the width and height divisible by 2
        subimage = cv.GetSubRect(timg, (0, 0, sz[0], sz[1]))

        # down-scale and upscale the image to filter out the noise
        cv.PyrDown(subimage, pyr, 7)
        cv.PyrUp(pyr, subimage, 7)
        tgray = cv.CreateImage(sz, 8, 1)
        # find squares in every color plane of the image
        for c in range(3):
            # extract the c-th color plane
            channels = [None, None, None]
            channels[c] = tgray
            cv.Split(subimage, channels[0], channels[1], channels[2], None)
            for l in range(N):
                # hack: use Canny instead of zero threshold level.
                # Canny helps to catch squares with gradient shading
                if (l == 0):
                    cv.Canny(tgray, gray, 0, thresh, 5)
                    cv.Dilate(gray, gray, None, 1)
                else:
                    # apply threshold if l!=0:
                    #     tgray(x, y) = gray(x, y) < (l+1)*255/N ? 255 : 0
                    cv.Threshold(tgray, gray, (l + 1) * 255 / N, 255, cv.CV_THRESH_BINARY)

                # find contours and store them all as a list
                contours = cv.FindContours(gray, storage, cv.CV_RETR_LIST, cv.CV_CHAIN_APPROX_SIMPLE)

                if not contours:
                    continue

                contour = contours
                totalNumberOfContours = 0
                while (contour.h_next() != None):
                    totalNumberOfContours = totalNumberOfContours + 1
                    contour = contour.h_next()
                # test each contour
                contour = contours
                # print 'total number of contours %d' % totalNumberOfContours                                                # debug
                contourNumber = 0

                while (contourNumber < totalNumberOfContours):

                    # print 'contour #%d' % contourNumber                                                # debug
                    # print 'number of points in contour %d' % len(contour)                                                # debug
                    contourNumber = contourNumber + 1

                    # approximate contour with accuracy proportional
                    # to the contour perimeter
                    result = cv.ApproxPoly(contour, storage,
                                           cv.CV_POLY_APPROX_DP, cv.ArcLength(contour) * 0.02, 0)

                    # square contours should have 4 vertices after approximation
                    # relatively large area (to filter out noisy contours)
                    # and be convex.
                    # Note: absolute value of an area is used because
                    # area may be positive or negative - in accordance with the
                    # contour orientation
                    if (len(result) == 4 and
                                abs(cv.ContourArea(result)) > 500 and
                            cv.CheckContourConvexity(result)):
                        s = 0
                        for i in range(5):
                            # find minimum angle between joint
                            # edges (maximum of cosine)
                            if (i >= 2):
                                t = abs(self.__angle(result[i % 4], result[i - 2], result[i - 1]))
                                if s < t:
                                    s = t
                        # if cosines of all angles are small
                        # (all angles are ~90 degree) then write quandrange
                        # vertices to resultant sequence
                        if (s < 0.3):
                            pt = [result[i] for i in range(4)]
                            squares.append(pt)
                            print ('current # of squares found %d' % len(squares))
                    contour = contour.h_next()

        if call_tracking:  debugprt(self, currentframe(), pgm, 'end   ')
        return squares

    def GetImage(self, drawROIs=False, selection=None, crosses=None, timestamp=False):
        if call_tracking: debugprt(self, currentframe(), pgm, 'begin     ')  # debug
        """
        class Monitor
        
        GetImage(self, drawROIs = False, selection=None, timestamp=0)

        drawROIs       False        (Default)   Will draw all ROIs to the image
                       True

        selection      (x1,y1,x2,y2)            A four point selection to be drawn

        crosses        (x,y),(x1,y1)            A list of tuples containing single point coordinates

        timestamp      True                     Will add a timestamp to the bottom right corner
                       False        (Default)

        Returns the last collected image
        """
        self.imageCount += 1

        try: frame = self.cam.getImage(timestamp)
        except: print("GetImage @ 1645 failed. Check paths and filenames.")


        if frame:

            if timestamp: frame = self.__drawFPS(frame)
            if self.tracking: frame = self.doTrack(frame, show_raw_diff=False, drawPath=self.drawPath)

            if drawROIs and self.arena.ROIS:
                ROInum = 0
                for ROI, beam in zip(self.arena.ROIS, self.arena.beams):
                    ROInum += 1
                    frame = self.__drawROI(frame, ROI, ROInum=ROInum)
                    frame = self.__drawBeam(frame, beam)

            if selection:
                frame = self.__drawROI(frame, selection, color=(0, 0, 255))

            if crosses:
                for pt in crosses:
                    frame = self.__drawCross(frame, pt, color=(0, 0, 255))

            if self.grabMovie: cv.WriteFrame(self.writer, frame)

        else:
#            sys.stdout = open(console_file, 'w')  # send console output to file
            print('$$$$$$ pysolovideo: monitor: getimage: NOT frame     ----------- so done!')

            cv2.waitKey()

            sys.exit()

        if call_tracking: debugprt(self, currentframe(), pgm, 'end   ')
        return frame

    def processFlyMovements(self):
        if call_tracking:  debugprt(self, currentframe(), pgm, 'begin     ')  # debug
        """
        Decides what to do with the data
        Called every frame
        """
        ct = self.getFrameTime()
        self.__tempFPS += 1
        delta = (ct - self.lasttime)

        # if delta >= 1: # if one-half second has elapsed
        self.lasttime = ct
        self.arena.compactSeconds(self.__tempFPS, delta)  # average the coordinates and transfer from buffer to array
        self.processingFPS = self.__tempFPS;
        self.__tempFPS = 0
        # endif

        if call_tracking:  debugprt(self, currentframe(), pgm, 'end   ')

    def showimg(self, title, img):  # displays an image                 # debug
        img_nparry = np.asarray(img[:, :])
        cv2.imshow(title, img_nparry)
        cv2.waitKey()
        cv2.imwrite(data_dir + 'snapshots\\' + title + '.jpg', img_nparry)

    def doTrack(self, frame, show_raw_diff=False, drawPath=True):
        if call_tracking: debugprt(self, currentframe(), pgm, 'begin     count = ')

        """
        Track flies in ROIs using findContour algorithm in opencv
        Each frame is compared against the moving average
        take an opencv frame as input and return a frame as output with path, flies and mask drawn on it
        """

        self.count += 1

        if show_imgs: self.showimg('1703 frame count = ' + str(self.count), frame)
        track_one = True  # Track only one fly per ROI
        # print('$$$$$$, pysolovideo, dotrack, 1737, count = ,', self.count)

        # Smooth to get rid of false positives
        cv.Smooth(frame, frame, cv.CV_GAUSSIAN, 3, 0)
        # if show_imgs:  self.showimg('1708 smooth frame ' + str(self.count), frame)    

        # Create some empty containers to be used later on
        grey_image = cv.CreateImage(cv.GetSize(frame), cv.IPL_DEPTH_8U, 1)
        # if show_imgs: self.showimg('1712 grey image ' + str(self.count), grey_image)    

        temp = cv.CloneImage(frame)
        # if show_imgs: self.showimg('1715 temp ' + str(self.count), temp)    

        difference = cv.CloneImage(frame)
        # if show_imgs: self.showimg('1718 difference ' + str(self.count), difference)    

        ROImsk = cv.CloneImage(grey_image)
        # if show_imgs: self.showimg('1721 ROImsk ' + str(self.count), ROImsk)    

        ROIwrk = cv.CloneImage(grey_image)
        # if show_imgs: self.showimg('1724 ROIwrk ' + str(self.count), ROIwrk)    


        if self.__firstFrame:
            # create the moving average
            self.moving_average = cv.CreateImage(cv.GetSize(frame), cv.IPL_DEPTH_32F, 3)
            # if show_imgs: self.showimg('1730 moving_average ' + str(self.count), self.moving_average)    

            cv.ConvertScale(frame, self.moving_average, 1.0, 0.0)
            # if show_imgs: self.showimg('1733 ConvertScale moving_average ' + str(self.count), self.moving_average)    

            self.__firstFrame = False
        else:
            # update the moving average
            cv.RunningAvg(frame, self.moving_average, 0.2, None)  # 0.04
            # if show_imgs: self.showimg('1739 RunningAvg moving_average ' + str(self.count), self.moving_average)    

        # Convert the scale of the moving average.
        cv.ConvertScale(self.moving_average, temp, 1.0, 0.0)
        # if show_imgs: self.showimg('1744 ConvertScale moving_average ' + str(self.count), self.moving_average)    


        # Minus the current frame from the moving average.
        cv.AbsDiff(frame, temp, difference)
        if show_imgs: self.showimg('1749 AbsDiff difference ' + str(self.count), difference)

        # Convert the image to grayscale.
        cv.CvtColor(difference, grey_image, cv.CV_RGB2GRAY)
        # if show_imgs: self.showimg('1754 CvtColor grey_image ' + str(self.count), grey_image)    


        # Convert the image to black and white.
        cv.Threshold(grey_image, grey_image, 20, 255, cv.CV_THRESH_BINARY)
        # if show_imgs: self.showimg('1759 Threshold grey_image ' + str(self.count), grey_image)    

        # Dilate and erode to get proper blobs
        cv.Dilate(grey_image, grey_image, None, 2)  # 18
        # if show_imgs: self.showimg('1763 Dilate grey_image ' + str(self.count), grey_image)    

        cv.Erode(grey_image, grey_image, None, 2)  # 10
        if show_imgs: self.showimg('1765 Erode grey_image ' + str(self.count), grey_image)

        # Build the mask. This allows for non rectangular ROIs
        for ROI in self.arena.ROIS:
            cv.FillPoly(ROImsk, [ROI], color=cv.CV_RGB(255, 255, 255))
            if show_imgs: self.showimg('1772 FillPoly ROImsk  ' + str(self.count) + 'ROI' + str(ROI), ROImsk)

        # Apply the mask to the grey image where tracking happens
        cv.Copy(grey_image, ROIwrk, ROImsk)
        if show_imgs: self.showimg('1776 grey_image ' + str(self.count), grey_image)
        if show_imgs: self.showimg('1777 ROIwrk ' + str(self.count), ROIwrk)
        if show_imgs: self.showimg('1778 ROImsk ' + str(self.count), ROImsk)

        storage = cv.CreateMemStorage(0)

        # track each ROI
        for fly_number, ROI in enumerate(self.arena.ROIStoRect()):
            # print('$$$$$$, pysolovideo, dotrack, 1794, for ROI number ' + str(fly_number) + ', frame ' + str(self.count))                                    # debug
            (x1, y1), (x2, y2) = ROI
            cv.SetImageROI(ROIwrk, (x1, y1, x2 - x1, y2 - y1))
            cv.SetImageROI(frame, (x1, y1, x2 - x1, y2 - y1))
            cv.SetImageROI(grey_image, (x1, y1, x2 - x1, y2 - y1))

            contour = cv.FindContours(ROIwrk, storage, cv.CV_RETR_CCOMP, cv.CV_CHAIN_APPROX_SIMPLE)

            points = []
            fly_coords = None

            while contour:
                # Draw rectangles
                bound_rect = cv.BoundingRect(list(contour))
                contour = contour.h_next()
                if track_one and not contour:  # this will make sure we are tracking only the biggest rectangle
                    pt1 = (bound_rect[0], bound_rect[1])
                    pt2 = (bound_rect[0] + bound_rect[2], bound_rect[1] + bound_rect[3])
                    points.append(pt1);
                    points.append(pt2)
                    cv.Rectangle(frame, pt1, pt2, cv.CV_RGB(255, 0, 0), 1)

                    fly_coords = (pt1[0] + (pt2[0] - pt1[0]) / 2, pt1[1] + (pt2[1] - pt1[1]) / 2)
                    area = (pt2[0] - pt1[0]) * (pt2[1] - pt1[1])
                    if area > 400:
                        fly_coords = None
                        # print('$$$$$$, pysolovideo, dotrack, 1810, area > 400 - no coords, area = ',area)

            # for each frame adds fly coordinates to all ROIS. Also do some filtering to remove false positives
            fly_coords, distance = self.arena.addFlyCoords(fly_number, fly_coords)

            frame = self.__drawCross(frame, fly_coords)
            if drawPath: frame = self.__drawLastSteps(frame, fly_number, steps=5)
            if show_raw_diff: grey_image = self.__drawCross(grey_image, fly_coords, color=(100, 100, 100))

            cv.ResetImageROI(ROIwrk)
            cv.ResetImageROI(grey_image)
            cv.ResetImageROI(frame)

        self.processFlyMovements()

        if show_raw_diff:
            temp2 = cv.CloneImage(grey_image)
            cv.CvtColor(grey_image, temp2, cv.CV_GRAY2RGB)  # show the actual difference blob that will be tracked
            if show_imgs: self.showimg(
                '1829 diff blob being tracked, ' + str(self.count) + ' fly # ' + str(str(fly_number)), temp2)

            if call_tracking:  debugprt(self, currentframe(), pgm, 'end   ')
            return temp2

        if call_tracking:  debugprt(self, currentframe(), pgm, 'end   ')
        return frame
