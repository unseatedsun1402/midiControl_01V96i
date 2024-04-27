# midiControl_01V96i
---- New Version in Java ----
In March 2024, I decided to try to move this project to java instead of python for the slight performance benefits and more industry standard web service support.
This Version has been tested as working with one way communication to the desk and supports the 01V96 Mixer (mix 1-8 is on controlled on 9-16) and the M7CL mixer
---- Python version currently undeveloped ----

Python program using pygame to connect to Yamaha 01V96i Digital mixing desk and provide control over Midi for various parameters

Currently under heavy development and non-functional

When the program is capable of sending and recieving meaningful data (i.e. can make changes to the desk setting) then the project will enter preRelease.

When the ui is functional then the project will be under alpha release.

Goals for Version 1.0:
  *A program that can read desk parameters live and display them as well as allowing the user to make changes to the settings.
  
  *A graphical user interface emulating real-world controls (such as knobs and faders)
  
  *A server function for multiple simultaneous mobile devices to make edits/see parameters live.
