# -*- coding: utf-8 -*-
"""
Created on Sun Oct 02 08:19:10 2016

@author: laughreyl
"""

sys.stdout = open('d:\\DAM_Analysis\\stdout.txt', 'w')                                                  # DEBUG

sys.stdout.close()
sys.stdout = open("/dev/stdout", "w")