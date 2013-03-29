This will let you control PyMOL using a game controller. This is in pre-alpha
stage currently. Still todo are the following:

Support more than one game controller
Support xbox 360 controllers (currently these crash in windows)
have a dead zone so that while game controllers aren't used they dont interfere
with mouse input and fire off unnecessary redraws in PyMOL.


Installation and use

pygameSplinter.py needs to be run independently of Pymol from python and 
requires pygame to be installed. These needs to keep running while collabmol 
is running from within PyMOL


WiiMOL_Plugin.py needs to be copied into PyMOLs tk startup plugins directory 
or installed using the plugin installtion interface in PyMOL. To use the plugin
simply start it from the menu
 