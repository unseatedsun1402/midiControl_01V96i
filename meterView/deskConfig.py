import inputChannel, AUXchannel, BUSchannel, stereoBus

def setup(type = None):
    # M7CL Config
    inp = {inputChannel for i in range(47)}
    bus = {BUSchannel for i in range(15)}
    aux = {BUSchannel for i in range(15)}

    # LS9-32 Config
    inp = {inputChannel for i in range(63)}
    bus = {BUSchannel for i in range(15)}
    aux = {BUSchannel for i in range(15)}

    # 01v96 Config
    inp = {inputChannel for i in range(31)}
    bus = {BUSchannel for i in range(7)}
    aux = {AUXchannel for i in range(7)}