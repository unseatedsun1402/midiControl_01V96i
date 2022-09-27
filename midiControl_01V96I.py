from distutils.log import info
import string
#import sys
#import os
import time
from tokenize import String
import pygame as pg
import pygame.midi
import csv
from warnings import catch_warnings

class Connection():
    """Connection is a class object that can access a midi device input and output"""
    input = pygame.midi.Input
    output = pygame.midi.Output

    
        
    def __init__(self, device):
        """When creating a connection object pass in the midi device input and output ports as a tuple to create the connections"""
        (input_id,output_id) = device
        self.input = pygame.midi.Input(input_id)
        self.output = pygame.midi.Output(output_id)
    

    

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

##-------select main input device--------##
def input_main(device_id=None):
    pg.init()

    pygame.midi.init()

    _print_device_info()

    if device_id is None:
        input_id = pygame.midi.get_default_input_id()
    else:
        input_id = device_id

    print(f"using input_id :{input_id}:")
    i = pygame.midi.Input(input_id)

    pg.display.set_mode((1, 1))

    going = True
    while going:
        events = pygame.event.get()
        for e in events:
            if e.type in [pg.QUIT]:
                going = False
            if e.type in [pg.KEYDOWN]:
                going = False
            if e.type in [pygame.midi.MIDIIN]:
                print(e)

        if i.poll():
            midi_events = i.read(10)
            # convert them into pygame events.
            midi_evs = pygame.midi.midis2events(midi_events, i.device_id)

            for m_e in midi_evs:
                pygame.event.post(m_e)

    del i
    pygame.midi.quit()


##--------main output device selection--------##
    '''def output_main(device_id=None):
        pg.init()
        pygame.midi.init()

        _print_device_info()

        if device_id is None:
            port = pygame.midi.get_default_output_id()
        else:
            port = device_id

        print(f"using output_id :{port}:")
        midi_out = pygame.midi.Output(port, 0)'''




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

    def __init__(self, cc):
        stripped_cc = cc[2:]
        self.cc = int(stripped_cc)
        self.name = cc
        self.checkme = 'awesome {}'.format(self.name)
    
    def __setValue__(self, val):
        self.faderVal = val
    
    def __faderRead__(self):
        self.faderLevel = int(self.faderLevel)

def createChannels(numberOfChannels: int):
    for i in range(numberOfChannels):
        instanceIDs.append('ch'+str(i))
    print(instanceIDs)

##--------fader control--------##
def getbytes(cc):
    values = bytearray
    level = input('Fader Value (0-1023)')
    level = int(level) % 1024
    dmod = divmod(level,128)
    byte1 = dmod[1]
    byte2 = dmod[0]
    values = [0x00,0x00,byte2,byte1]
    setFaderlvl(cc,values)

def setFaderlvl(cc,values):
    pygame.midi.init()
    bytes = bytearray
    bytes = [0xF0,0x43,0x10,0x3E,0x7F,0x01,0x1C,0x00,cc,values[0],values[1],values[2],values[3],0xF7]
    print(bytes)
    try:
        connection.output.write_sys_ex(msg= bytes,when= pygame.midi.time())
    except(pygame.midi.MidiException):
        print('failed')

def getFaderlvl(cc):
    bytes = bytearray
    bytes = [0xF0,0x43,0x30,0x3E,0x7F,0x01,0x1C,0x00,cc,0xF7]
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
                    print(message)
                reading = False
            elif reading:
                    message.append(byte)
    
    

    

instanceIDs = []
connection = Connection(find_01V96i_desk())
#establish_connection(find_01V96i_desk())
createChannels(40)
holder = {name: Channel(cc=name) for name in instanceIDs}
#print(holder['ch19'].cc)

getbytes(holder['ch5'].cc)
'''flag = True
while flag:
    for channel in holder:
        getbytes(holder[channel].cc)
    flag = False'''

#print(holder['ch39'].checkme)


getFaderlvl(holder['ch5'].cc)