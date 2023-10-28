"""Parses incoming midi messages"""
from Connection import Connection

class ResponseException(Exception):
    def __init__(self, *args):
         self.message = "Response not found"
         #return self.message
    

class Parser():
    input_events = []
    """parameter changes for input objects"""
    bus_events = []
    """parameter changes for bus objects"""
    AUX_events = []
    """parameter changes for AUX objects"""
    output_events = []
    """parameter changes for output objects"""
    settings_events = []
    """parameter changes for settings objects"""
    stereo_events = []
    """parameter changes for stereo bus objects"""

    connection = Connection

    def __init__(self,conn: Connection):
        self.connection = conn
        ## replace constant F0,43,3E/30,10 with runtime defined constant for wider desk compatability

    def _readBytes(self,bufferSize: int):
        events = self.connection.input.read(bufferSize)
        
        return events
    
    def listen(self):
        '''listens for desk changes and returns valid messages to the calling function'''
        resolution = []
        inputMeter = []
        AUXMeter = []
        BusMeter = []
        #MatrixMeter = []
        StereoMeter = []

        events = self.connection.input.read(128)
        cursor = 0
        for event in range(len(events)):
            for each in events[event]:
                if(isinstance(each,int) != True):
                    if set([0xF0,0x43,0x10,0x3E]).issubset(each):
                        try:
                            end = False
                            bite = events[cursor][0]
                            message = []
                            while not end:
                                cursor += 1
                                bite = events[cursor][0]
                                if (0xF7 in bite):
                                     message.append(bite)
                                     end = True
                                else:
                                     message.append(bite)
                            if len(message) > 2:
                                if set([0x1A,0x21]).issubset(message[1][:2]):
                                    res = message[2][0],(128*message[2][1])+message[2][2]
                                    match(message[1][2:]):
                                        case[0x00,0x00]:
                                            inputMeter.append(res)
                                        case[0x01,0x00]:
                                            AUXMeter.append(res)
                                        case[0x02,0x00]:
                                            BusMeter.append(res)
                                        case[0x04,0x00]:
                                            StereoMeter.append((res[1],(128*message[2][3])+message[3][0]))
                                else:
                                    if(message[0] != [0xF0,0x43,0x10,0x3E]):
                                        message.insert(0,[0xF0,0x43,0x10,0x3E])
                                    if message[1] != [0x1a, 0x21, 0x4, 0x0]:
                                        resolution.append(message)
                                     
                        except IndexError as e:
                            #print (e)
                            pass
                else:
                    pass
                    break
            cursor += 1
        
        returnVal = (inputMeter,AUXMeter,BusMeter,StereoMeter,resolution)
        return (returnVal)
    
    def listenFor(connection,*args):
        direction = args[0]
        param = args[1]
        cc = args[2]
        

        response = []
        found = False
        events = connection.input.read(256)
        for event in range(len(events)-2):
            for each in events[event]:
                if(isinstance(each,int) != True):
                    if direction == each:
                        next = [item for item in events[event+1][0]]
                        

                        if set(param).issubset(next):
                            data = [item for item in events[event+2][0]]
                            if (data[0] == cc):
                                found = True
                                for item in events[event+3][0]:
                                    data.append(item)
                                return data
        if not found :
             raise ResponseException('Information not found')

             
             

    def update_meters(self):
        """collects meter value updates"""
        events = self.connection.input.read(1024)
        inputMeter = []
        AUXMeter = []
        BusMeter = []
        #MatrixMeter = []
        StereoMeter = []

        started = False
        for event in range(len(events)):
            for each in events[event]:
                if(isinstance(each,int) != True):
                    if set([0xF0,0x43,0x10,0x3E]).issubset(each):
                        try:
                            next = events[event+1][0]
                            data = events[event+2][0]
                            data2 = events[event+3][0]
                            res = (data[0],(128*data[1])+data[2])
                            if next == [0x1A,0x21,0x00,0x00]:
                                    inputMeter.append(res)
                            
                            elif next == [0x1A,0x21,0x01,0x00]:
                                    BusMeter.append(res)
                                
                            elif next == [0x1A,0x21,0x02,0x00]:
                                    AUXMeter.append(res)
                            
                            elif next == [0x1A,0x21,0x04,0x00]:
                                    StereoMeter.append((res[1],(128*data[3])+data2[0]))
                                #case 0x53:
                                #    MatrixMeter.append(tuple(id = each[8],data = [each[9],each[10],each[11],each[12]]))
                        except IndexError as e:
                            #print (e)
                            pass
                else:
                    pass
                    break
        
        res = (inputMeter,BusMeter,AUXMeter,StereoMeter)
        return (res)
