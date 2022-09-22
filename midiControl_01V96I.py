from distutils.log import info
import sys
import os
import time
import pygame as pg
import pygame.midi
import csv
from warnings import catch_warnings

def connection():
    in_id = int
    out_id = int

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
    def output_main(device_id=None):
        pg.init()
        pygame.midi.init()

        _print_device_info()

        if device_id is None:
            port = pygame.midi.get_default_output_id()
        else:
            port = device_id

        print(f"using output_id :{port}:")
        midi_out = pygame.midi.Output(port, 0)

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

def establish_connection(device):
    (input_id, output_id) = device
    #print('Input id:', input_id)
    pygame.midi.init()
    '''for i in range(pygame.midi.get_count()):
        try:
            
                print(pygame.midi.Input(i).poll())
        except(pygame.midi.MidiException):
            print('nothing')
    try:    #tests connection is successful and fails gracefully else
        conn = pygame.midi.Input(input_id)
            

        if conn.poll():
            print('Connection OK')
            connection.in_id=input_id
            connection.out_id=output_id
    except(pygame.midi.MidiException):
        print("Connection Failed")'''
    
    #poll for master bus level
    'F0	43	30	3E	1A	21	04	00	7F	00	01	F7'
    outConn = pygame.midi.Output(output_id)
    conn = pygame.midi.Input(input_id,buffer_size=256)
    while True:
        outConn.write_sys_ex(0,[0xF0,0x43,0x30,0x3E,0x1A,0x21,0x04,0x00,0x7F,0x00,0x01,0xF7])
        time.sleep(1)
        for i in range(3):
            dataToProcess = list
            dataToProcess = conn.read(1)
            print(dataToProcess[0][0])
            dataObj = bytes(dataToProcess[0][0])
            print(dataObj)
        time.sleep(3)




##--------populate meter values--------##
#with open('METER_DATA.csv','r')as csv_file:
#    csv_reader = csv.DictReader(csv_file)

##--------pull meter data--------##

#establish_connection()
establish_connection(find_01V96i_desk())