from distutils.log import error
import pygame.midi as midi
# from tkinter import *

class Connection():
    """Connection is a class object that can access a midi device input and output"""
        
    def __init__(self):
        """When creating a connection object pass in the midi device input and output ports as a tuple to create the connections"""

        device = find_01V96i_desk()
        (input_id,output_id) = device
        try:
            self.input = midi.Input(input_id)
            self.output = midi.Output(output_id)
        except:
            error("Midi Device not Found")

def find_01V96i_desk():
    '''finds the mixing desk in the midi interfaces'''
    midi.init()
    findA = b'Yamaha 01V96i Port1'
    input_id = -1
    output_id = -1

    nofdevices = midi.get_count()
    for i in range(nofdevices):
        device = midi.get_device_info(i)
        
        (interf, name, input, output, opened) = device
        name += b'_' # padding to ensure 'in' operation evalate to true if term == target
        if findA in name:
            if input == 1:
                input_id = i
            if output == 1:
                output_id = i
    midi.quit
    device = (input_id,output_id)
    return(device)