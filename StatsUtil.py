# -*- coding: utf-8 -*-
"""
Created on Fri Dec 23 13:24:11 2022

@author: mbelani
"""

import time

class StatsUtil:
    """
    Simple class to keep track of execution time. Start time is set to the
    time of object creation, whereas end time is handled in the destructor
    (i.e., when the object is descoped/deleted).
    """
    
    def __init__(self):
        self.start_time = time.time()
        
    def __del__(self):
        # Print the elapsed execution time
        print("\nThis took %.3f seconds." % (time.time() - self.start_time))
