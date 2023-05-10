"""Parses incoming midi messages"""
from Connection import Connection

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

    def _readBytes(self,bufferSize: int):
        events = self.connection.input.read(bufferSize)
        
        return events
    
    def listen(self):
        events = self._readBytes
        eventFlag = 0
        for event in events:
            for each in event:
                if set([0xF0,0x43,0x10,0x3E,0x7f,0x01]).issubset(each):
                    eventFlag = 1
                    if each[6] >= 0 and each[6] < 27:
                        self.input_events.append(each)
                    elif each[6] >= 27 and each[6] < 34:
                        self.bus_events.append(each)
                    elif each[6] >= 34 and each[6] < 41:
                        self.AUX_events.append(each)
                    elif each[6] >= 0x4b and each[6] < 0x56:
                        self.stereo_events.append(each)
        return eventFlag

    def update_meters(self):
        """collects meter value updates"""
        events = self.connection.input.read(256)
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
                            data = events[event+3][0]
                            res = (data[0],[data[1],data[2],data[3],data[0]])
                            if next == [0x1A,0x04,0x50,0x00]:
                                    inputMeter.append(res)
                            
                            elif next == [0x1A,0x04,0x51,0x00]:
                                    BusMeter.append(res)
                                
                            elif next == [0x1A,0x04,0x52,0x00]:
                                    AUXMeter.append(res)
                            
                            elif next == [0x1A,0x04,0x54,0x00]:
                                    StereoMeter.append(res)
                                #case 0x53:
                                #    MatrixMeter.append(tuple(id = each[8],data = [each[9],each[10],each[11],each[12]]))
                        except Exception as e:
                            print (e)
                else:
                    pass
                    break
        
        res = (inputMeter,BusMeter,AUXMeter,StereoMeter)
        return (res)
