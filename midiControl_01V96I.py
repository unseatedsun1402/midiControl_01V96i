from distutils.log import info
import sys
import os
import time
from warnings import catch_warnings

import pygame as pg
import pygame.midi

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
    find = b'Yamaha 01V96i-1'
    input_id = int
    output_id = int
    for i in range(pygame.midi.get_count()):
        device = pygame.midi.get_device_info(i)
        (interf, name, input, output, opened) = device
        if name==find:
            if input:
                input_id = i
            if output:
                output_id = i
    return(input_id,output_id)

def establish_connection():
    device = find_01V96i_desk()
    (input_id, output_id) = device
    print('Input id:', input_id)
    pygame.midi.init()
    conn = pygame.midi.Input(input_id)
    while True:
        conn.poll()
        #print('Connection OK')
        time.sleep(.1)

#print(find_01V96i_desk())
establish_connection()