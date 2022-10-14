from ast import pattern
from distutils.log import info
import string
import sys
from sys import argv
#import os
import time
from tokenize import String
import pygame as pg
import pygame.midi
import csv
from warnings import catch_warnings
from tkinter import *
from tkinter import ttk

from pyparsing import Char

class Connection():
    """Connection is a class object that can access a midi device input and output"""
    input = pygame.midi.Input
    output = pygame.midi.Output

    
        
    def __init__(self, device):
        """When creating a connection object pass in the midi device input and output ports as a tuple to create the connections"""
        (input_id,output_id) = device
        try:
            self.input = pygame.midi.Input(input_id)
            self.output = pygame.midi.Output(output_id)
        except:
            root = Tk()
            frm = ttk.Frame(root, padding=10)
            frm.grid()
            ttk.Label(frm, text="Device not found. Please check device connections and drivers are up to date.").grid(column=0, row=0)
            ttk.Button(frm, text="Quit", command=exit).grid(column=1, row=0)
            root.mainloop()


patterns = {
        (240, 67, 16, 62, 127, 1, 79,0):"master fader",
        (0xF0,0x43,0x10,0x3E,0x7F,0x01,0x1A,0x00):"channel on",
        (240, 67, 16, 62, 26, 4, 90, 0):"channel on",
        (0xf0,0x43,0x10,0x3e,0x7f,0x01,0x1b,0x00):"channel pan",
        (0xf0,0x43,0x10,0x3e,0x7f,0x01,0x1c,0x00):"fader",
        (0xf0,0x43,0x10,0x3e,0x7f,0x01,0x1c,0x00):"fader",
        (0xf0,0x43,0x10,0x3e,0x7f,0x01,0x1c,0x01):"fader fade",
        (0xf0,0x43,0x10,0x3e,0x7f,0x01,0x1d,0x00):"channel attenuator",
        (0xf0,0x43,0x10,0x3e,0x7f,0x01,0x1d,0x01):"channel attenuator bit-shift ",
        (0xF0,0x43,0x10,0x3E,0x7F,0x01,0x23,0x00):"aux 1 on",
        (0xF0,0x43,0x10,0x3E,0x7F,0x01,0x23,0x02):"aux 1 pre",
        (0xF0,0x43,0x10,0x3E,0x7F,0x01,0x23,0x03):"aux 1 lvl",
        (0xF0,0x43,0x10,0x3E,0x7F,0x01,0x23,0x04):"aux 2 on",
        (0xF0,0x43,0x10,0x3E,0x7F,0x01,0x23,0x05):"aux 2 pre",
        (0xF0,0x43,0x10,0x3E,0x7F,0x01,0x23,0x06):"aux 2 lvl",
        (0xF0,0x43,0x10,0x3E,0x7F,0x01,0x23,0x07):"aux 3 on",
        (0xF0,0x43,0x10,0x3E,0x7F,0x01,0x23,0x08):"aux 3 pre",
        (0xF0,0x43,0x10,0x3E,0x7F,0x01,0x23,0x08):"aux 3 lvl",
        (0xF0,0x43,0x10,0x3E,0x7F,0x01,0x23,0x09):"aux 4 on",
        (0xF0,0x43,0x10,0x3E,0x7F,0x01,0x23,0x0a):"aux 4 pre",
        (0xF0,0x43,0x10,0x3E,0x7F,0x01,0x23,0x0b):"aux 4 lvl",
        (0xF0,0x43,0x10,0x3E,0x7F,0x01,0x23,0x0c):"aux 5 on",
        (0xF0,0x43,0x10,0x3E,0x7F,0x01,0x23,0x0d):"aux 5 pre",
        (0xF0,0x43,0x10,0x3E,0x7F,0x01,0x23,0x0e):"aux 5 lvl",
        (0xF0,0x43,0x10,0x3E,0x7F,0x01,0x23,0x0f):"aux 6 on",
        (0xF0,0x43,0x10,0x3E,0x7F,0x01,0x23,0x10):"aux 6 pre",
        (0xF0,0x43,0x10,0x3E,0x7F,0x01,0x23,0x11):"aux 6 lvl",
        (0xF0,0x43,0x10,0x3E,0x7F,0x01,0x23,0x12):"aux 7 on",
        (0xF0,0x43,0x10,0x3E,0x7F,0x01,0x23,0x13):"aux 7 pre",
        (0xF0,0x43,0x10,0x3E,0x7F,0x01,0x23,0x14):"aux 7 lvl",
        (0xF0,0x43,0x10,0x3E,0x7F,0x01,0x23,0x15):"aux 8 on",
        (0xF0,0x43,0x10,0x3E,0x7F,0x01,0x23,0x16):"aux 8 pre",
        (0xF0,0x43,0x10,0x3E,0x7F,0x01,0x23,0x17):"aux 8 lvl",
        (0xF0,0x43,0x10,0x3E,0x7F,0x01,0x1F,0x01):"input compressor on",
        (0xF0,0x43,0x10,0x3E,0x7F,0x01,0x1E,0x00):"input gate on",
        (0xF0,0x43,0x10,0x3E,0x7F,0x01,0x20,0x0F):"input eq on",
        (240, 67, 16, 62, 26, 4, 92, 0):"aux bus on",
        (240, 67, 16, 62, 26, 4, 91, 0):"mix bus on",
        (240, 67, 16, 62, 26, 4, 9, 23):"layer select",
        (240, 67, 16, 62, 26, 3, 46, 0):"solo ch on",
        (240, 67, 16, 62, 26, 3, 46, 1):"cue/solo safe",
        (240, 67, 16, 62, 26, 3, 46, 2):"cue/solo total",
        (240, 67, 16, 62, 26, 4, 48, 0):"solo local",
        (240, 67, 16, 62, 26, 4, 48, 1):"solo global",
        (240, 67, 16, 62, 26, 4, 48, 2):"solo inout local",
        (240, 67, 16, 62, 26, 4, 48, 3):"solo inout global",
        (240, 67, 16, 62, 26, 3, 47, 0):"solo master on",
        (240, 67, 16, 62, 26, 3, 47, 1):"solo master on bk",
        (240, 67, 16, 62, 26, 3, 47, 2):"solo master total on",
        (240, 67, 16, 62, 26, 4, 9, 24):"select channel"
    }

    

##--------print midi devices---------##
def print_device_info():
    pygame.midi.init()
    _print_device_info()
    pygame.midi.quit()

def _print_device_info():
    for i in range(pygame.midi.get_count()):
        r = pygame.midi.get_device_info(i)
        (interf, name, input, output, opened) = r

        in_out = ""
        if input:
            in_out = "(input)"
        if output:
            in_out = "(output)"

        print(
            "%2i : port : interface :%s:, name :%s:, opened :%s:  %s"
            % (i, interf, name, opened, in_out)
        )
#print_device_info()

##--------return Midi Input and Output ports--------##
'''finds the mixing desk in the midi interfaces'''
def find_01V96i_desk():
    pygame.midi.init()
    findA = b'Yamaha 01V96i-1'
    findB = b'2- Yamaha 01V96i-1'
    input_id = -1
    output_id = -1
    for i in range(pygame.midi.get_count()):
        device = pygame.midi.get_device_info(i)
        (interf, name, input, output, opened) = device
        if name==findA or name == findB:
            if input:
                input_id = i
            if output:
                output_id = i
    pygame.midi.quit
    return(input_id,output_id)






##--------populate meter values--------##
with open('METER_DATA.csv','r')as csv_file:
    csv_reader = csv.DictReader(csv_file)

##--------pull meter data--------##


##--------create channel objects--------##
class Channel:
    """The channel object is used to store input channel paramters for each channel.
    Channels are accessed primarily through the cc as this is unique to each input channel and names can be duplicated."""
    cc = int
    """input channel"""
    name = string
    """channel name"""
    faderVal = int
    """current fader position (0-1023"""
    faderOn = int
    """channel On or Off"""

    def __init__(self, name):
        self.cc = int(name[2:])
        self.name = name
        self.checkme = 'awesome {}'.format(self.name)
        self.pattern = {'meter':[0xf0,0x43,0x30,0x3e,0x1a,0x21,0x00,0x01,self.cc,0x00,0x01],
                    'fader':[0xF0,0x43,0x30,0x3E,0x7F,0x01,0x1C,0x00,self.cc],
                    'name':[0xF0,0x43,0x30,0x3E,0x1A,0x02,0x04,0x04,self.cc]
                    }
    
    def setFaderValue(self, channel, value):
        (byte2,byte1) = value
        pygame.midi.init()
        bytes = list(self.pattern['fader'])
        bytes.append(byte2)
        bytes.append(byte1)
        bytes.append(0xf7)
        print(bytes)
        try:
            connection.output.write_sys_ex(msg= bytes,when= pygame.midi.time())
            self.faderVal = value
        except(pygame.midi.MidiException):
            print('failed')
    
    def getFader(self):
        bytes = bytearray
        bytes = list(self.pattern['fader'])
        bytes.append(0xf7)
        connection.output.write_sys_ex(msg= bytes,when= pygame.midi.time())
        time.sleep(0.05)
        message = []
        reading = False
        for event in connection.input.read(256):
            for byte in event[0]:
                if byte == 0xf0:
                    if not reading:
                        message = [event[0][0]]
                        reading = True
                elif byte == 0xf7 and reading:
                    if len(message) > 12:
                        return(message[11],message[12])
                    reading = False
                elif reading:
                        message.append(byte)
    
    def getMeter(self):
        bytes = []
        bytes = list(self.pattern['meter'])
        bytes.append(0xf7)
        connection.output.write_sys_ex(msg= bytes,when= pygame.midi.time())
        time.sleep(0.05)
        message = []
        reading = False
        for event in connection.input.read(256):
            for byte in event[0]:
                if byte == 0xf0:
                    if not reading:
                        message = [event[0][0]]
                        reading = True
                elif byte == 0xf7 and reading:
                    if len(message) > 10:
                        #connection.input.close()
                        return(message[9],message[10])
                    reading = False
                elif reading and len(message) <15:
                        message.append(byte)
                else: reading = False
        #connection.input.close()

    def getName(self):
        bytes = []
        bytes = list(self.pattern['name'])
        bytes.append(0xf7)
        name = String
        for i in range(15):
            connection.output.write_sys_ex(msg= bytes,when= pygame.midi.time())
            bytes[7] += 1
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

    


def createChannels(numberOfChannels: int):
    for i in range(numberOfChannels):
        instanceIDs.append('ch'+str(i))
    print(instanceIDs)


##--------Aux Controls--------##
class Aux():

    def __init__(self,name):
        self.cc = int(name[2:])
        """To change/request a parameter follow the end of the bytearray with the cc and data (if required)"""
        self.pattern = {
            "change":[0xF0,0x43,0x10,0x3E,0x7F,0x01,0x23,self.cc],
            "request":[0xF0,0x43,0x30,0x3E,0x7F,0x01,0x23,self.cc],
            "fader change":[0xF0,0x43,0x10,0x3E,0x7F,0x01,0x39,0x00,self.cc],
            "fader request":[0xF0,0x43,0x10,0x3E,0x7F,0x01,0x39,0x00,self.cc],
            "default":[0x06,0x55]
        }
        self.name = "aux" + str(self.cc//3)

    def getSendLevel(self,channel):
        bytes = list(self.pattern["request"])
        bytes.append(channel.cc)
        bytes.append(0xf7)
        connection.output.write_sys_ex(when=pygame.midi.time(),msg=bytes)
        time.sleep(0.05)
        message = []
        reading = False
        for event in connection.input.read(256):
            for byte in event[0]:
                if byte == 0xf0:
                    if not reading:
                        message = [event[0][0]]
                        reading = True
                elif byte == 0xf7 and reading:
                    if len(message) > 12:
                        print(message)
                    reading = False
                elif reading:
                        message.append(byte)
    def sendLevel(self,channel,value):
        pygame.midi.init()
        (byte2,byte1) = value
        bytes = bytearray
        bytes = list(self.pattern['change'])
        bytes.append(channel.cc)
        bytes.append(0x00)
        bytes.append(0x00)
        bytes.append(byte2)
        bytes.append(byte1)
        bytes.append(0xf7)
        #print(bytes)
        try:
            connection.output.write_sys_ex(msg= bytes,when= pygame.midi.time())
        except(pygame.midi.MidiException):
            print('failed')


def createAuxChannels(numberOfChannels: int):
    for i in range(numberOfChannels):
        auxIDs.append('cc'+str(i))

    

instanceIDs = []
auxIDs = []
connection = Connection(find_01V96i_desk())
#establish_connection(find_01V96i_desk())
createChannels(40)
createAuxChannels(24)
channels = {name: Channel(name=name) for name in instanceIDs}
auxChannels = {name: Aux(name=name) for name in auxIDs}
#print(auxChannels['cc3'].pattern['request'])
#print(auxChannels['cc2'].name)
auxChannels['cc2'].getSendLevel(channels['ch0'])

#for channel in channels:
    #print(channels[channel].getFader())

#while True:
#for channel in channels:
#    print(channels[channel].getMeter())

print(channels['ch6'].getName())
#print(channels['ch19'].cc)
#getbytes(channels['ch5'])
'''flag = True
while flag:
    for channel in channels:
        getbytes(channels[channel].cc)
    flag = False'''

#print(channels['ch39'].checkme)
##--------incomming event handler--------##
class SysexEvent:
    def __init__(self,msg):
        self.msg = msg
        self.classify()
    
    def classify(self):
        msg = self.msg
        patt = []
        for i in range(8):
            patt.append(msg[i])
        try:
            print(patterns[tuple(patt)],"ch"+ str(msg[8]))
            self.type = patterns[tuple(patt)]
        except KeyError:
            print("unkown",msg)
            hexval = []
            for each in patt:
                hexval.append(hex(each))
            #print(hexval)


##--------listens to the desk--------##
def changeListener():
    def listen():
        while True:
            message = []
            reading = False
            if connection.input.poll():
                for event in connection.input.read(256):
                    for byte in event[0]:
                        if byte == 0xf0:
                            if not reading:
                                message = [event[0][0]]
                                reading = True
                        elif byte == 0xf7 and reading:
                            if len(message) > 12:
                                return(message)
                            reading = False
                        elif reading:
                                message.append(byte)
    while True:
        event = SysexEvent(listen())
        argv.clear()
        
argv.clear()
print("Args ",argv)
changeListener()
