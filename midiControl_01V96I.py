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
    return(input_id,output_id)

def establish_connection():
    device = find_01V96i_desk() #returns input and output id
    (input_id, output_id) = device
    connection.in_id = input_id
    connection.out_id = output_id
    pygame.midi.init()
    try:    #tests connection is successful and fails gracefully else
        conn = pygame.midi.Input(connection.in_id)
        if conn.poll():
            print('Connection OK')
    except(pygame.midi.MidiException):
        print("Connection Failed")


##--------populate meter values--------##
with open('METER_DATA.csv','r')as csv_file:
    csv_reader = csv.DictReader(csv_file)

##--------pull meter data--------##
def get_stereo_level():
    ''''''

##--------send fader position--------##
def push_fader_level(int):
    pygame.midi.init()
    print(pygame.midi.get_count())
    pygame.midi.Output.write_sys_ex(10,msg=[0xF0,0x43,0x31,0x3E,0x7F,0x01,0x32,0x01,0xcc,0xF7],when=pygame.midi.time())
    pygame.midi.quit()
#push_fader_level(0)

##--------channel on--------##
def channel_on():
    pygame.midi.init()
    print(pygame.midi.Input(1).poll())
    pygame.midi.Output(10).write_sys_ex(msg=[0xF0,0x43,0x11,0x3E,0x1A,0x20,0x00,0x00,0x00,0xdd,0xF7], when=pygame.midi.time())

establish_connection()
channel_on()