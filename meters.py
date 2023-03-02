import mido
from errno import errorcode
from distutils.log import error
import pygame as pg
import pygame.midi as midi
import time
from tkinter import *

##--------Starting Variables-------##
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

def find_01V96i_desk():
    '''finds the mixing desk in the midi interfaces'''
    midi.init()
    findA = b'Yamaha 01V96i-1'
    findB = b'2- Yamaha 01V96i-1'
    input_id = -1
    output_id = -1
    for i in range(midi.get_count()):
        device = midi.get_device_info(i)
        (interf, name, input, output, opened) = device
        if name==findA or name == findB:
            if input:
                input_id = i
            if output:
                output_id = i
    midi.quit
    return(input_id,output_id)

class inputChannel():
    def __init__(self,val):
        self.id = val
        self.short = self.__get_short()
        self.name = self.__get_name()
        
    
    def __get_short(self):
        """Gets short (xxxx) channel name"""
        msg = bytearray[0xF0,0x43,0x30,0x3E,0x1A,0x02,0x04,0x00,self.id]
        msg.append(0xf7)

        for i in range(3):
            connection.output.write_sys_ex(msg= msg,when= midi.time())
            msg[7] += 1
            time.sleep(0.1)
            message = []
            reading = False
            for event in connection.input.read(256):
                for byte in event[0]:
                    if byte == 0xf0:
                        if not reading:
                            message = [event[0][0]]
                            reading = True
                    elif byte == 0xf7 and reading and len(message) > 6:

                        if message[6] == 4:
                            #connection.input.close()
                            print(chr(message[len(message)-1]))
                            reading = False
                        else:
                            pass
                    elif reading and len(message) <15:
                            message.append(byte)
                    else: reading = False

    def __get_name(self):
        """Gets long channel name"""
        msg = bytearray[0xF0,0x43,0x30,0x3E,0x1A,0x02,0x04,0x04,self.cc]
        msg.append(0xf7)

        for i in range(15):
            connection.output.write_sys_ex(msg= msg,when= midi.time())
            msg[7] += 1
            time.sleep(0.1)
            message = []
            reading = False
            for event in connection.input.read(256):
                for byte in event[0]:
                    if byte == 0xf0:
                        if not reading:
                            message = [event[0][0]]
                            reading = True
                    elif byte == 0xf7 and reading and len(message) > 6:
                        if message[6] == 4:
                            #connection.input.close()
                            print(chr(message[len(message)-1]))
                            reading = False

                        else:
                            pass
                    elif reading and len(message) <15:
                            message.append(byte)
                    else: reading = False

    def update_meter(self,point: int):
        """polls meter value meter value data"""
        connection.output.write(data= bytearray[0xf0,0x43,0x30,0x3e,0x1a,0x21,0x00,0x01,self.id,0x00,0xf1])



try:
    connection = Connection(find_01V96i_desk())
    INPUT =  {i:inputChannel(i) for i in range(40)}
    print("done")
except:
    error("Connection failed")