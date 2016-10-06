# -*- coding: utf-8 -*-
"""
Created on Wed Oct 05 21:10:47 2016

@author: laughreyl
"""

from inspect import currentframe, getframeinfo
import inspect
import os, datetime

def debugprt(self,cf,pgm,header):

    timestp = "{:%y-%m-%d %H:%M:%S}".format(datetime.datetime.now())
#    datetime.datetime.now().format('%Y-%m-%d %H:%M:%S')

    a = inspect.getframeinfo(cf)
    funcname = a[2]
    lineno = cf.f_lineno 
    filename = os.path.split(a[0])[1]
    print(timestp + "\t " + header + "\t\t" + funcname + "\t\t" + str(lineno) + "\t\t" + filename )

#   insert into code:    debugprt(currentframe(),pgm)
