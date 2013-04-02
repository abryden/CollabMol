Installation:
1. Make sure you have python installed and install PyMOL for windows using
the installation instructions found at: 

http://www.pymolwiki.org/index.php/Windows_Install

2. install Pygame using the appropriate installer found at:

http://www.lfd.uci.edu/~gohlke/pythonlibs/#pygame

3. Follow the directions to enable plugins in PyMOL at:

http://www.pymolwiki.org/index.php/Windows_Install

4. Download the zip archive of CollabMol from github:

https://github.com/abryden/CollabMol

5. Unpack the zip file

6. Install the file "CollabMol_Plugin.py" using the plugin manager in PyMOL

7. Turn on all the game controllers you want to use

8. Double click on "pygameSplinter.py" to launch it using python (which has pygame installed)

9. 


This will let you control PyMOL using a game controller. This is in pre-alpha
stage currently. Still todo are the following:

## DONE Support more than one game controller
## DONE Support xbox 360 controllers (currently these crash in windows)
##DONE have a dead zone so that while game controllers aren't used they dont interfere
## DONE with mouse input and fire off unnecessary redraws in PyMOL.


Installation and use

pygameSplinter.py needs to be run independently of Pymol from python and 
requires pygame to be installed. These needs to keep running while collabmol 
is running from within PyMOL


WiiMOL_Plugin.py needs to be copied into PyMOLs tk startup plugins directory 
or installed using the plugin installtion interface in PyMOL. To use the plugin
simply start it from the menu
 