# -*- coding: utf-8 -*-
"""
Created on Fri Oct 28 22:23:09 2016

@author: Lori
"""

import codecs

x1 = 10
x_width = 20
x_sep = 3

y1 = 20
y_height = 20
y_sep = 3

rows = 2
columns = 3

filename = 'C:\\Users\\laughreyl\\Documents\\GitHub\\LL-DAM-Analysis\\Data\\automask.msk'

fh = open(filename,'w')

# %%              Write header and first row

ax = x1                     # create the four corners of the first box
ay = y1                     #
bx = x1 + x_width             #   A(x,y)  B(x,y)
by = y1                     #   D(x,y)  C(x,y)
cx = x1 + x_width
cy = y1 + y_height
dx = x1
dy = y1 + y_height
ROI = 1

# outstr = '(lp1\n((I%d\nI%d\nt(I%d\nI%d\nt(I%d\nI%d\nt(I%d\nI%d\n' % (ax,ay,bx,by,cx,cy,dx,dy)
fh.write(  '(lp1\n((I%d\nI%d\nt(I%d\nI%d\nt(I%d\nI%d\nt(I%d\nI%d\n' % (ax,ay,bx,by,cx,cy,dx,dy))

for col in range(0,columns):        # x-coordinates changes through columns
    ax = ax + x_width + x_sep       # move to the right in x
    ay = y1                         # reset y-coordinate to start of row
    bx = bx + x_width + x_sep
    by = y1
    cx = cx + x_width + x_sep
    cy = y1
    dx = dx + x_width + x_sep
    dy = y1
    for row in range(0,rows):       # y-coordinates changes through rows
        ay = ay + y_height + y_sep
        by = by + y_height + y_sep
        cy = cy + y_height + y_sep
        dy = dy + y_height + y_sep
        ROI = ROI + 1
#         outstr = 'ttp%d\na((I%d\nI%d\nt(I%d\nI%d\nt(I%d\nI%d\nt(I%d\nI%d\n' % (ROI,ax,ay,bx,by,cx,cy,dx,dy)
        fh.write('ttp%d\na((I%d\nI%d\nt(I%d\nI%d\nt(I%d\nI%d\nt(I%d\nI%d\n' % (ROI,ax,ay,bx,by,cx,cy,dx,dy))

# no           fh.write('ttp%d\naI%d\nI%d\nI%d\nI%d\n%d\n%d\n%d\n%d\n' % (ROI,ax,ay,bx,by,cx,cy,dx,dy))
# no            fh.write('ttp%d\na(I%d\nI%d\nI%d\n%d\n%d\n%d\n%d\n%d\n' % (ROI,ax,ay,bx,by,cx,cy,dx,dy))
# works        fh.write('ttp%d\naI%d\nI%d\nI%d\n%d\n%d\n%d\n%d\n%d\n' % (ROI,ax,ay,bx,by,cx,cy,dx,dy))
# works        fh.write('ttp%d\naI%d\nI%d\nI%d\n text %d\n%d\n%d\n%d\n%d\n' % (ROI,ax,ay,bx,by,cx,cy,dx,dy))
# works        fh.write('ttp%d \naI%d \nI%d \nI%d \n%d \n%d \n%d \n%d \n%d \n' % (ROI,ax,ay,bx,by,cx,cy,dx,dy))
# works        fh.write('ttp%d \na((I%d \nI%d \nI%d \n%d \n%d \n%d \n%d \n%d \n' % (ROI,ax,ay,bx,by,cx,cy,dx,dy))


       
# outstr = 'ttp%d\na.(lp1\nI1\n' % (ROI+1)
fh.write('ttp%d\na.(lp1\nI1\n' % (ROI+1))
#
#outstr = 'aI1\n'*(rows*columns)  + 'a.' 
fh.write('aI1\n'*(rows*columns)) 
fh.write('a.')        
        
fh.close()
