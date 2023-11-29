import inputChannel, AUXchannel, BUSchannel, stereoBus, Connection
from AUXchannel import auxChannel
from BUSchannel import busChannel
from inputChannel import inputChannel

def setup(conn = None,type = None):
    if(conn == None):
        conn = Connection()

    match(type):
        # M7CL Config
        case('m7cl'):   
            inp = {i:inputChannel(i, conn,AUXCOUNT = 16, BusCOUNT=16) for i in range(48)}
            aux = {i:auxChannel(i,conn = conn) for i in range(16)}
            bus = {i:busChannel(i,conn = conn) for i in range(16)}

        # LS9-32 Config
        case('LS9-32'):
            inp = {i:inputChannel(i, conn,AUXCOUNT = 16, BusCOUNT=16) for i in range(64)}
            aux = {i:auxChannel(i,conn = conn) for i in range(16)}
            bus = {i:busChannel(i,conn = conn) for i in range(16)}

        # 01v96 Config
        case('01V96i'):
            inp = {i:inputChannel(i, conn,AUXCOUNT = 8, BusCOUNT=8) for i in range(32)}
            aux = {i:auxChannel(i,conn = conn) for i in range(8)}
            bus = {i:busChannel(i,conn = conn) for i in range(8)}
    
    return(inp,bus,aux)