# -*- coding: utf-8 -*-
"""
Created on Thu Dec 22 22:32:41 2022

@author: mbelani
"""

class Utilities:
    def __init__ (self):
        print("In init")

    @staticmethod    
    def format_seconds(num_seconds):
        """
        Parameters
        ----------
        num_seconds : numeric
            The number of seconds to be converted to the various time
            components (weeks/days/hours/mins/secs).

        Returns
        -------
        string
            seconds converted to weeks/days/hours/minutes/seconds returned
            as a string.

        """
        nweeks = 0
        ndays = 0
        nhours = 0
        nminutes = 0
        time_pieces = []
        
        num_seconds = int(num_seconds)
        
        # Compute (mathematically) the number of seconds, minutes, hours,
        # days, weeks
        if num_seconds >= 60:
            nminutes = num_seconds // 60
            num_seconds -= nminutes * 60
        
        if num_seconds > 0:
            time_pieces.insert(0, str(num_seconds) + " seconds")

        if nminutes > 60:
            nhours = nminutes // 60
            nminutes -= nhours * 60

        if nminutes > 0:
            time_pieces.insert(0, str(nminutes) + " minutes")

        if nhours > 24:
            ndays = nhours // 24
            nhours -= ndays * 24

        if nhours > 0:
            time_pieces.insert(0, str(nhours) + " hours")

        if ndays > 7:
            nweeks = ndays // 7
            ndays -= nweeks * 7

        if ndays > 0:
            time_pieces.insert(0, str(ndays) + " days")
            
        if nweeks > 0:
            time_pieces.insert(0, str(nweeks) + " weeks")
                        
        return ", ".join(time_pieces)

