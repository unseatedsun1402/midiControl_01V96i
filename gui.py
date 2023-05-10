import midiControl_01V96I
from tkinter import *
from tkinter import ttk

from tkinter import *
from tkinter import ttk

#default values
pageTitle = 'Selected Channel'



root = Tk()
root.config(bg='#DDDDFA')
root.geometry('300x200')
root.title('Main')


#styles
default = ttk.Style()
selected = ttk.Style()
# Create style used by default for all Frames
default.configure('TFrame', background='#1A1AAA')
selected.configure('selected.TFrame', background='#404040')



mainView = ttk.Frame(root,style = 'TFrame')
#mainView.config(bg='#FFFAFA')
mainView['borderwidth'] = 2
mainView['relief'] = 'sunken'
page = ttk.Label(mainView,text=pageTitle)
page.grid(row=0,column=0,sticky=[N+E+W])

mainView.rowconfigure(0,weight=1)
mainView.columnconfigure(0,weight=1)
mainView.grid(column=0,row=0,sticky=[N+S+E+W])


secondaryView = ttk.Frame(root,style='selected.TFrame')
secondaryView['borderwidth'] = 2
secondaryView['relief'] = 'sunken'

navigation = ttk.Label(secondaryView,text='Master')
navigation.grid(row=0,column=0,sticky=[N+E+W])

secondaryView.rowconfigure(0,weight=1)
secondaryView.columnconfigure(0,weight=1)
secondaryView.grid(column=1,row=0,sticky=[N+S+E+W])

root.rowconfigure(0,weight=1)
root.columnconfigure(0,weight=3)
root.columnconfigure(1,weight=1)

root.mainloop()