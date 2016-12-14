# -*- coding: utf-8 -*-
"""
Created on Fri Oct 28 22:23:09 2016

@author: Lori
"""
rows = 8                    #  Chrimson/+ section
columns = 12

filename = 'C:\\Users\\laughreyl\\Documents\\GitHub\\LL-DAM-Analysis\\Data\\Working_files\\automask.msk'

fh = open(filename,'w')

# %%    Whole
"""
x1 = 21
x_len = 18
x_sep = 5.55
x_tilt = -.6

y1 = 71
y_len = 16
y_sep = 2.13
y_tilt = .44
"""
# %%    Upper Left column 1
"""
x1 = 21
x_len = 18
x_sep = 5.55
x_tilt = -.4

y1 = 67
y_len = 16
y_sep = 1.6
y_tilt = .4

"""
# %%    Upper Left column 7
"""
x1 = 163
x_len = 18
x_sep = 5.55
x_tilt = -.6

y1 = 70
y_len = 16
y_sep = 1.6
y_tilt = .5
"""
# %%    Lower Left column 7
"""
x1 = 158
x_len = 18
x_sep = 5.55
x_tilt = -.5

y1 = 238
y_len = 16
y_sep = 1.6
y_tilt = .5
"""
# %%    Upper Right first half
"""
x1 = 351
x_len = 18
x_sep = 5.55
x_tilt = -.4

y1 = 75
y_len = 16
y_sep = 1.6
y_tilt = .4
"""
# %%    Upper Right second half
"""
x1 = 515
x_len = 18
x_sep = 5.55
x_tilt = -.4

y1 = 79
y_len = 16
y_sep = 1.6
y_tilt = .4
"""
# %%    Upper Right middle third
"""
x1 = 355 + 4*(18+5.55)
x_len = 18
x_sep = 5.55
x_tilt = -.4

y1 = 76
y_len = 16
y_sep = 1.6
y_tilt = .4
"""
# %%    Lower Right
""""""
x1 = 350
x_len = 18
x_sep = 5.55
x_tilt = -.4

y1 = 242
y_len = 16
y_sep = 1.6
y_tilt = .4
""""""

ROI = 1

for row in range(0, rows):  # y-coordinates change through rows
    ax = x1 + row * x_tilt  # reset x-coordinate start of row
    bx = ax + x_len
    cx = bx
    dx = ax
    if row == 0:
        ay = y1
    else:
        ay = y1 + row * (y_len + y_sep)  # move down in y
    by = ay
    cy = ay + y_len
    dy = cy
    for col in range(0, columns):  # x-coordinates change through columns
        if (col == 0 and row == 0):
            fh.write('(lp1\n((I%d\nI%d\nt(I%d\nI%d\nt(I%d\nI%d\nt(I%d\nI%d\n' % (ax, ay, bx, by, cx, cy, dx, dy))
            print('(lp1\n((I%d\nI%d\nt(I%d\nI%d\nt(I%d\nI%d\nt(I%d\nI%d\n' % (ax, ay, bx, by, cx, cy, dx, dy))
        else:
            fh.write('ttp%d\na((I%d\nI%d\nt(I%d\nI%d\nt(I%d\nI%d\nt(I%d\nI%d\n' % (ROI, ax, ay, bx, by, cx, cy, dx, dy))
            print('ttp%d\na((I%d\nI%d\nt(I%d\nI%d\nt(I%d\nI%d\nt(I%d\nI%d\n' % (ROI, ax, ay, bx, by, cx, cy, dx, dy))
        ax = bx + x_sep
        bx = ax + x_len
        cx = bx
        dx = ax
        ay = ay + y_tilt
        by = ay
        cy = ay + y_len
        dy = cy
        ROI = ROI + 1


fh.write('ttp%d\na.(lp1\nI1\n' % (ROI+1))

fh.write('aI1\n'*(rows*columns-1)) 
fh.write('a.\n\n\n')
        
fh.close()
