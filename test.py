import midiControl_01V96I
from sys import argv
from sys import stderr
from sys import stdout

if(len(argv) > 1):
    func = argv[1]
    eval('midiControl_01V96I.'+func+'()')
    if(len(argv) >= 2):
        print(func(argv[2]))
    else:
        print(func)
else:
    stderr.write("Error: No Arguments given")