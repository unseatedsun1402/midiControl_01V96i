"""Parses incoming midi messages"""
import Connection

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

    def __init__(self,conn: Connection):
        self.connection = conn

    def _readBytes(self,bufferSize: int):
        events = []
        for each in self.connection.input.read(bufferSize):
            events.append(each)
        
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
        events = self._readBytes(256)
        inputMeter = []
        AUXMeter = []
        BusMeter = []
        MatrixMeter = []
        StereoMeter = []


        for event in events:
            for each in event:
                if set([0xF0,0x43,0x10,0x3E,0x1A,0x04]).issubset(each):
                    match each[6]:
                        case 0x50:
                            inputMeter.append(tuple(id = each[8],data = [each[9],each[10],each[11],each[12]]))
                        
                        case 0x51:
                            BusMeter.append(tuple(id = each[8],data = [each[9],each[10],each[11],each[12]]))
                        
                        case 0x52:
                            AUXMeter.append(tuple(id = each[8],data = [each[9],each[10],each[11],each[12]]))
                        
                        case 0x53:
                            MatrixMeter.append(tuple(id = each[8],data = [each[9],each[10],each[11],each[12]]))

                        case 0x54:
                            StereoMeter.append(tuple(id = each[8],data = [each[9],each[10],each[11],each[12]]))

                        case _:
                            pass
                else:
                    break
        
        
        return tuple(inputMeter,BusMeter,AUXMeter,MatrixMeter,StereoMeter)
