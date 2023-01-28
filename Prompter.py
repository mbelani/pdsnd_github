# -*- coding: utf-8 -*-
"""
Created on Thu Dec 22 11:07:07 2022

@author: mbelani
"""

class Prompter:
    """
    Simple class to prompt user for baskc input (city name, month name, etc.)
    """

    def __init__(self, item, prompt, valid_list, allow_all):
        self.__item__ = item
        self.__prompt__ = "Enter one of the following " + prompt
        if allow_all:
            self.__prompt__ += "(enter 'all' for all) "
        self.__prompt__ += "- " + ", ".join(valid_list) + ": "
        self.__valid_list__ = valid_list
        self.__allow_all__ = allow_all
        self.__input_value__ = None

    @property
    def item(self):
        return self.__item__
    
    @property
    def prompt(self):
        return self.__prompt__
    
    @property
    def valid_list(self):
        return self.__valid_list__
    
    @property
    def allow_all(self):
        return self.__allow_all__
    
    @property
    def input_value(self):
        return self.__input_value__
    
    def getinput(self):
        """
        Prompts the user for input; continues in a loop (until valid input
        is received).
        
        Returns
        -------
        string
            actual input value (e.g., city name) that is entered by the user

        """
        done = False
        inputval = None
    
        while not done:
            inputval = input(self.prompt)
            inputval = inputval.lower()
            
            if inputval in self.valid_list:
                # All good; we got a valid item
                done = True
                self.__input_value__ = inputval
            else:
                print('{} is not a recognized value for {}. Please re-enter.'
                      .format(inputval, self.item))

        return self.input_value
