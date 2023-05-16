"""Yamaha digital mixer virtual input channel object"""
import Connection, VU
import time
import pygame.midi as midi
import pygame

sysExChg = [0xF0,0x43,0x10,0x3E]
sysExReq = [0xf0,0x43,0x30,0x3e]

class inputChannel():
    """Yamaha digital mixer virtual stereo bus object"""
    connection = Connection

    def __init__(self,val: int,conn: Connection):
        """Pass connection"""
        self.connection = conn
        self.id = val
        self.level = 0
        
    
    '''def __get_short(self):
        """Gets short (xxxx) channel name"""
        msg = [0xF0,0x43,0x30,0x3E,0x1A,0x02,0x04,0x00,self.id]
        msg.append(0xf7)
        message = ['1','2','3','4']
        i = 0
        while i <= 3:
            self.connection.output.write_sys_ex(msg= msg,when= midi.time())
            msg[7] = i
            time.sleep(0.001)
            sysex = []
            reading = False
            buffer = self.connection.input.read(256)
            for events in range(len(buffer)-1):
                try:
                    if not reading:
                        if set(sysExChg).issubset(buffer[events][0]):
                            #message[i] = events[0].append(list(each for each in events[0]))
                            reading = True
                            for each in buffer[events][0]:
                                sysex.append(each)
                    elif [0x1a,0x02,0x04,i] == buffer[events][0]:
                        for each in buffer[events][0]:
                            sysex.append(each)
                        if set([self.id,0x00,0x00]).issubset(buffer[events+1][0]):
                            message[i] = chr(buffer[events+2][0][0])
                            i += 1
                            reading = False
                            sysex = []
                    else:
                        reading = False
                        sysex = []
                except Exception as e:
                    print(e)
        name = ''
        for each in message:
            name = name + each
        return (name)

    def __get_name(self):
        """Gets long channel name"""
        msg = [0xF0,0x43,0x30,0x3E,0x1A,0x02,0x04,0x00,self.id]
        msg.append(0xf7)
        message = [str(each) for each in range(16)]
        i = 4
        while i < 20:
            self.connection.output.write_sys_ex(msg= msg,when= midi.time())
            msg[7] = i
            time.sleep(0.001)
            sysex = []
            reading = False
            buffer = self.connection.input.read(256)
            for events in range(len(buffer)-1):
                try:
                    if not reading:
                        if set(sysExChg).issubset(buffer[events][0]):
                            #message[i] = events[0].append(list(each for each in events[0]))
                            reading = True
                            for each in buffer[events][0]:
                                sysex.append(each)
                    elif [0x1a,0x02,0x04,i] == buffer[events][0]:
                        for each in buffer[events][0]:
                            sysex.append(each)
                        if set([self.id,0x00,0x00]).issubset(buffer[events+1][0]):
                            message[i-4] = chr(buffer[events+2][0][0])
                            i += 1
                            reading = False
                            sysex = []
                    else:
                        reading = False
                        sysex = []
                except Exception as e:
                    print(e)
        name = ''
        for each in message:
            name = name + each
        return (name)'''

    def get_status(self):
        """polls meter value meter value data"""
        self.connection.output.write_sys_ex(msg = [0xF0,0x43,0x30,0x3E,0x1A,0x21,0x05,0x00,self.id,0x00,0x01,0xf7],when=midi.time())

    def update_level(self,data):
        self.level = (data)
        return True
    
    def draw(self,context):
        """draws a meter for given input"""
        
        segment = 0
        for i in range (884,self.level, 256):
            if (i>4096):
                break
            segment += 1
            if i < 3000: 
                pygame.draw.rect(context, (0, 192, 0), ((self.id%16 *30)+7, ((1+(self.id//16))*210)-(segment*5)-2, 10, 5))
            elif i >= 3000 and i < 4000:
                pygame.draw.rect(context, (255, 200, 0), ((self.id%16 *30)+7, ((1+(self.id//16))*210)-(segment*5)-2, 10, 5))
            else:
                pygame.draw.rect(context, (255, 0, 0), ((self.id%16 *30)+7, ((1+(self.id//16))*210)-(segment*5)-2, 10, 5))