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
            print "got some Data!"
            dataStorage = data

	    length = struct.unpack_from("i",data)[0]
	    #print length
	    firstData = struct.unpack_from("i" + length * "fffffffffffffffff",data)
	    Rotate(-firstData[2],-firstData[1])
	    #print firstData



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
