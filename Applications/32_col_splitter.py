# -*- coding: utf-8 -*-
"""
Created on Thu Nov 03 16:53:14 2016

@author: laughreyl
"""
import numpy as np

inputfile = 'C:\\Users\\laughreyl\\Documents\\GitHub\\LL-DAM-Analysis\\Data\\20160823_135217\\1fps_run\\Monitor1_orig.txt'
outputfile = 'C:\\Users\\laughreyl\\Documents\\GitHub\\LL-DAM-Analysis\\Data\\20160823_135217\\1fps_run\\File_' + str(filenum)

fhin = open(inputfile,'r')
txt = fhin.readline()
# num_files = int(((len(txt)-34)/82)+0.499)
fhout = open(outputfile,'w')

with open(inputfile,'r') as fhin:
    txt = fhin.readline()
    for i in range(1,140):
        print(i, txt[0:i])
    
    
    
    
#    fhout.write(txt)
fhin.close()
fhout.close()
    
    
