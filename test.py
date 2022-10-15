##--------Aux Controls--------##
from curses import keyname
from subprocess import call


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
#connection = Connection(find_01V96i_desk())
#establish_connection(find_01V96i_desk())
#createChannels(40)
createAuxChannels(24)
#channels = {name: Channel(name=name) for name in instanceIDs}
auxChannels = {name: Aux(name=name) for name in auxIDs}
#print(auxChannels['cc3'].pattern['request'])
#print(auxChannels['cc2'].name)

returnArgs = ((str(auxChannels.keys()))[10:]).strip(')')

print((getattr(auxChannels,'keys')))