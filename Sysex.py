'''Sysex is a Python Object used for requesting and changing parameter values via sysex on Yamaha Mixing Consoles'''
import pygame
import pygame.midi

class Request:
    '''Request Class Object: Sends a Sysex Message requesting a specific parameter value'''
    def getFader(self):
        pygame.midi.Output(self.out).write_sys_ex(0,[0xf0,0x43,0x30,0x3e,0x7f,0x01,0x1c,0x00,self.cc,0xf7])

class Change:
    1