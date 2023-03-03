from distutils.log import error
import pygame.midi as midi
from tkinter import *

class Connection():
    """Connection is a class object that can access a midi device input and output"""
        
    def __init__(self, device):
        """When creating a connection object pass in the midi device input and output ports as a tuple to create the connections"""
        (input_id,output_id) = device
        try:
            self.input = midi.Input(input_id)
            self.output = midi.Output(output_id)
        except:
            error("Midi Device not Found")
            root = Tk()
            errNotice = Label(root, text="Device not found. Please check device connections and drivers are up to date.").grid(column=0, row=0)
            exitBtn = Button(root, text="Quit", command= exit).grid(column=0, row=1)


            root.mainloop()