import os
import sys
import Tkinter
from Tkinter import *
import tkFileDialog
import subprocess
from pymol import cmd




from thread import *

import os
import sys
import pickle

from pymol import cmd
import pymol


import socket
import struct
import threading



import math
import time
		
def multMatrices(m1,m2):
	if len(m1) == 9 and len(m2) == 9:
		res = [0,0,0,0,0,0,0,0,0]
		for i in range(0,3):
			for j in range(0,3):
				res[3*i+j] = m1[3*i]*m2[j] + m1[3*i+1]*m2[j+3] + m1[3*i+2]*m2[j+6]
				
		return res


	
def matToQuat(m):
	q = [0,0,0,0]
	q[0] = math.sqrt( max( 0, 1 + m[0] + m[4] + m[8] ) ) / 2
	q[1] = math.sqrt( max( 0, 1 + m[0] - m[4] - m[8] ) ) / 2
	q[2] = math.sqrt( max( 0, 1 - m[0] + m[4] - m[8] ) ) / 2
	q[3] = math.sqrt( max( 0, 1 - m[0] - m[4] + m[8] ) ) / 2
	
	if (math.fabs(m[7] - m[5]) > 0):
		q[1] = q[1] * (m[7] - m[5]) / math.fabs(m[7] - m[5])
	if (math.fabs(m[2] - m[6]) > 0):
		q[2] = q[2] * (m[2] - m[6]) / math.fabs(m[2] - m[6])
	if (math.fabs(m[3] - m[1]) > 0):
		q[3] = q[3] * (m[3] - m[1]) / math.fabs(m[3] - m[1])
	
	return q
	

def quatToMat(q):
	m = [1,0,0,0,1,0,0,0,1]

	W = q[0]
	X = q[1]
	Y = q[2]
	Z = q[3]

	xx = X * X
	xy = X * Y
	xz = X * Z
	xw = X * W

	yy = Y * Y
	yz = Y * Z
	yw = Y * W

	zz = Z * Z
	zw = Z * W

	m[0] = 1 - 2 * ( yy + zz )
	m[1] = 2 * ( xy - zw )
	m[2] = 2 * ( xz + yw )

	m[3] = 2 * ( xy + zw )
	m[4] = 1 - 2 * ( xx + zz )
	m[5] = 2 * ( yz - xw )

	m[6] = 2 * ( xz - yw )
	m[7] = 2 * ( yz + xw )
	m[8] = 1 - 2 * ( xx + yy )

	return m



			
			

def rotateView(mat,angleX,angleY,angleZ):
	if len(mat) >= 9:	
		rotX = [1,0,0, 0,math.cos(angleX),-math.sin(angleX), 0,math.sin(angleX),math.cos(angleX)]
		rotY = [math.cos(angleY),0,math.sin(angleY), 0,1,0, -math.sin(angleY),0,math.cos(angleY)]
		rotZ = [math.cos(angleZ),-math.sin(angleZ),0, math.sin(angleZ),math.cos(angleZ),0, 0,0,1]

		rotXYZ = multMatrices(multMatrices(rotZ,rotY),rotX)
		rot_prev = []
		for i in range(0,9):
			rot_prev.append(mat[i])
			
		rot_new = multMatrices(rot_prev,rotXYZ)

		mat_new = []

		for i in range(0,9):
			mat_new.append(rot_new[i])
		for i in range(9,len(mat)):
			mat_new.append(mat[i])
			
		return mat_new
		
		




lastmovetime = 0.0
currentController = 0

def Rotate( angleX, angleY):
	#if not CheckMaster(controller):
	#	return
	currtime = time.clock()
	global lastmovetime
	#Slowdown code vvv - don't use for right now
	if ((currtime - lastmovetime) < .01):
	        #print "derp"
		return
	view = list(cmd.get_view())
	view = rotateView(view, angleX/20, angleY/20, 0)
	cmd.set_view(view)
	#DamageGUI()
	cmd.refresh()
	lastmovetime = time.clock()







Z_SPEED = 5
XY_SPEED = 10

def Translate(axis, distance0, distance1, dest):
	#Each controller must perform its own math for how to manipulate the distances and the axis.
	#if not CheckMaster(controller):
	#	return
	currtime = time.clock()
	#if( controller.lastTrans != axis or (controller.lastDist0 < 0 and distance0 > 0) or
	#									(controller.lastDist0 > 0 and distance0 < 0) or
	#									(controller.lastDist1 < 0 and distance1 > 0) or
	#									(controller.lastDist1 > 0 and distance1 < 0)):
	#	controller.startmovetime = currtime
	global lastmovetime
	delta = currtime - lastmovetime
	#controller.lastTrans = axis
	#controller.lastDist0 = distance0
	#controller.lastDist1 = distance1
	#Update 20x a second to avoid choppy chops. Note that any pymol induced lag will kill this.
	if (delta < .05):
		return

	#Because we're updating distances, we want a maximum speed as well...
	#The first frame after a period of non-movement shouldn't move.
	#if (delta > .25):
	#	delta = 0

	#coefficient = currtime - controller.startmovetime

	#Get the current view to manipulate the camera
	#The controller itself should handle the math to determine the distance it changes.
	#This merely translates
	view = list(cmd.get_view())
	if (axis == "Z"):
		distance0 = distance0  * Z_SPEED #*coefficient
		view[11] += distance0 * dest[2]
		
		view[9] += distance0 * dest[0]
		view[10] += distance0 * dest[1]
		
		view[15] -= distance0 * dest[2]
		view[16] -= distance0 * dest[2]
	if (axis == "XY"):
		distance0 = distance0 * XY_SPEED * .3*.004*(view[11]-view[14])# * coefficient
		distance1 = distance1 * XY_SPEED * .3*.004*(view[11]-view[14]) # * coefficient
		#Because X and Y are in relation to camera coordinates, we need to translate the object coordinates properly.
		#The real vector needs to be rotated:
		#Need to rotate by inverse of the camera's rotation matrix to line up X, Y properly with respect to camera
		#Inverse of orthogonal matrix = the transpose of the matrix
		# 0 3 6              0 1 2
		# 1 4 7 inverted is: 3 4 5
		# 2 5 8              6 7 8
		#            X part         Y part               Z part
		x = view[0] * distance0 + view[1] * distance1 #+ view[2] * 0
		y = view[3] * distance0 + view[4] * distance1 #+ view[5] * 0
		z = view[6] * distance0 + view[7] * distance1 #+ view[8] * 0

		view[12] -= x
		view[13] -= y
		view[14] -= z

	cmd.set_view(view)
	cmd.refresh()
	#global lastmovetime
	lastmovetime = time.clock()
	#DamageGUI()



def simpleTransZ(dist):
    	view = cmd.get_view()
	Translate( "Z", -1 * dist * 1  * 5,\
		  -1 * dist *  5,[0,0,1])

def simpleTransXY(dist1, dist2):
    Translate ("XY", dist1, dist2, [0,0,1])

class recieving_Thread(threading.Thread):
    running = 0
    def __init__(self):
        self.running = True
        self.sock = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
        print "failing to bind?"
	self.sock.bind( ("127.0.0.1",64324) )
        print "nope"
        threading.Thread.__init__(self)
    def run(self):
        while self.running:
            data, addr = self.sock.recvfrom( 1024 )
            #print "got some Data!"
            dataStorage = data

	    length = struct.unpack_from("i",data)[0]
	    #print str(length) + " length"
	    firstData = struct.unpack_from("i" + length * "ffffffffffffffffff",data)
	    numControllers = firstData[0]
	    #print str(numControllers) + " controllers"
	    
	    currtime = time.clock()

	    global currentController
	    global lastmovetime
	    #currentController = 1
	    #print str(currtime - lastmovetime) + " time delta"
	    if (currtime - lastmovetime) < .5:
		
		offset = currentController*18
		if(abs(firstData[1+offset]) < .25 and abs(firstData[2+offset]) < .25):
		    pass
		    #continue
		elif (firstData[10+offset] < .9 and firstData[5+offset] < .1):
		    Rotate(-firstData[2+offset],-firstData[1+offset])
		elif (firstData[10+offset] > .9):
		    simpleTransZ(firstData[2+offset])
		else:
		    simpleTransXY(-firstData[1+offset],firstData[2+offset])
	    #print firstData
	    else:
		for controller in range(0,numControllers):
		    currentController = controller
		    offset = currentController*18
		    if(abs(firstData[1+offset]) < .25 and abs(firstData[2+offset]) < .25):
			continue
		    #continue
		    elif (firstData[10+offset] < .9 and firstData[5+offset] < .1):
			Rotate(-firstData[2+offset],-firstData[1+offset])
			break
		    elif (firstData[10+offset] > .9):
			simpleTransZ(firstData[2+offset])
			break
		    else:
			simpleTransXY(-firstData[1+offset],firstData[2+offset])
			break



class WiiMOL:
	root = None
	def __init__(self):
		#self.bms = Bookmarks.Bookmarks()
		cmd.do("set label_color, yellow")
		cmd.do("set label_font_id, 4")
	#lock = allocate_lock()
		recievingThread = recieving_Thread()
		print "thread allocated"
		recievingThread.start()
		print "thread started"





def __init__(self):
	print self.winfo_id()
	self.menuBar.addcascademenu('Plugin','WiiMOL','WiiMOL',label = 'WiiMOL')
	self.menuBar.addmenuitem('WiiMOL','command','start WiiMOL', label = 'Start WiiMOL',command = lambda s = self: LoadWiiMOL(s))

	self.wiimol_running = False
                                     


def LoadWiiMOL(s):
	print "READY!"

	s.wiim = WiiMOL()
		
cmd.extend('loadWiiMOL',LoadWiiMOL)
