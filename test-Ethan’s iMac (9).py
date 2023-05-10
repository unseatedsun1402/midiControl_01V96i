import midiControl_01V96I
from sys import argv
from sys import stderr
from sys import stdout

while True:
    event = midiControl_01V96I.SysexEvent(midiControl_01V96I.listen())