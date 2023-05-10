from distutils.log import info
import sys
import os
import time
from warnings import catch_warnings

import pygame as pg
import pygame.midi

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

def establish_connection():
    device = find_01V96i_desk()
    (input_id, output_id) = device
    print('Input id:', input_id)
    pygame.midi.init()
    conn = pygame.midi.Input(input_id)
    while True:
        if conn.poll():
            print('Connection OK')
        time.sleep(.1)

#print(find_01V96i_desk())
establish_connection()