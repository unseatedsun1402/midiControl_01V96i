"""Yamaha digital mixer virtual input channel object"""
import Connection, VU
import time
import pygame.midi as midi

class inputChannel():
    """Yamaha digital mixer virtual input channel object"""
    connection = Connection

    def __init__(self,val: int,conn: Connection):
        """Pass an integer value to identify the channel"""
        self.id = val
        self.short = self.__get_short()
        self.name = self.__get_name()
        self.connection = conn
        self.level = 0
        self.meter = VU.Meter()        
    
    def __get_short(self):
        """Gets short (xxxx) channel name"""
        msg = bytearray[0xF0,0x43,0x30,0x3E,0x1A,0x02,0x04,0x00,self.id]
        msg.append(0xf7)

        for i in range(3):
            self.connection.output.write_sys_ex(msg= msg,when= midi.time())
            msg[7] += 1
            time.sleep(0.1)
            message = []
            reading = False
            for event in self.connection.input.read(256):
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
            self.connection.output.write_sys_ex(msg= msg,when= midi.time())
            msg[7] += 1
            time.sleep(0.1)
            message = []
            reading = False
            for event in self.connection.input.read(256):
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

    def get_status(self,point: int):
        """polls meter value meter value data"""
        self.connection.output.write(data= bytearray[0xF0,0x43,0x30,0x3E,0x1A,0x04,0x50,0x00,self.id,0xf1])

    def update_level(self,value):
        self.level = value

