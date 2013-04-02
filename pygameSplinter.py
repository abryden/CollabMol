
import pygame
import threading
import socket
import struct
import time
print "input finished"
import sys


exitnow = False

class joystickEventSender(threading.Thread):
    UDP_IP = "127.0.0.1"
    UDP_PORT = 64324
    controllers = []
    running = 1
    JoystickData = []
    sock = None;
    def __init__(self):
        pygame.init()
        pygame.joystick.init()
        for x in range(pygame.joystick.get_count()):
            pygame.joystick.Joystick(x).init()
            if(pygame.joystick.Joystick(x).get_numbuttons() == 15):
                self.controllers.append(1)
            else:
                self.controllers.append(0)
            self.JoystickData.append([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
       	threading.Thread.__init__(self)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    def run(self):
        while self.running:

	
	    


		time.sleep(.03);
		pygame.event.pump()
		for x in range(pygame.joystick.get_count()):
		    if(self.controllers[x] == 1):
			    #xbox 360
			print "xbox 360"
			self.JoystickData[x] =  [pygame.joystick.Joystick(x).get_axis(0),
					    pygame.joystick.Joystick(x).get_axis(1),
					    pygame.joystick.Joystick(x).get_axis(4) - pygame.joystick.Joystick(x).get_axis(5),
					    pygame.joystick.Joystick(x).get_axis(3),
					    pygame.joystick.Joystick(x).get_axis(2),
					    pygame.joystick.Joystick(x).get_button(11),
					    pygame.joystick.Joystick(x).get_button(12),
					    pygame.joystick.Joystick(x).get_button(13),
					    pygame.joystick.Joystick(x).get_button(14),
					    pygame.joystick.Joystick(x).get_button(8),
					    pygame.joystick.Joystick(x).get_button(9),
					    pygame.joystick.Joystick(x).get_button(5),
					    pygame.joystick.Joystick(x).get_button(4),
					    pygame.joystick.Joystick(x).get_button(6),
					    pygame.joystick.Joystick(x).get_button(7),
					    pygame.joystick.Joystick(x).get_button(3) - pygame.joystick.Joystick(x).get_button(2),
					    pygame.joystick.Joystick(x).get_button(0) - pygame.joystick.Joystick(x).get_button(1),
					    pygame.joystick.Joystick(x).get_button(10)]
		    else:
			    #logitech
			self.JoystickData[x] = [pygame.joystick.Joystick(x).get_axis(0),
						    pygame.joystick.Joystick(x).get_axis(1),
						    pygame.joystick.Joystick(x).get_button(6) - pygame.joystick.Joystick(x).get_button(7),
						    pygame.joystick.Joystick(x).get_axis(3),
						    pygame.joystick.Joystick(x).get_axis(2),
						    pygame.joystick.Joystick(x).get_button(1),
						    pygame.joystick.Joystick(x).get_button(2),
						    pygame.joystick.Joystick(x).get_button(0),
						    pygame.joystick.Joystick(x).get_button(3),
						    pygame.joystick.Joystick(x).get_button(4),
						    pygame.joystick.Joystick(x).get_button(5),
						    pygame.joystick.Joystick(x).get_button(8),
						    pygame.joystick.Joystick(x).get_button(9),
						    0,
						    0,
						    pygame.joystick.Joystick(x).get_hat(0)[0],
						    pygame.joystick.Joystick(x).get_hat(0)[1],
						    0]
	      #now that the data is fully updated, we send it off to the parent process.
	        #print "I'm working for now"
		self.send()
		global exitnow
		if exitnow:
		    for x in range(pygame.joystick.get_count()):
			pygame.joystick.Joystick(x).quit()
		    self.running = False
			
		    
		
    def send(self):
        formatString = "i" + len(self.controllers) * "ffffffffffffffffff"
        ##print formatString
        array = []
        #print self.JoystickData
        for i in self.JoystickData:
            for j in i:
                array.append(j);
        message = struct.pack(formatString, len(self.controllers),*array)
        #print struct.unpack_from("i",message)
        self.sock.sendto(message,(self.UDP_IP,self.UDP_PORT))
    #def quit():
	

thread = joystickEventSender()
try:
    thread.start()
    while True: time.sleep(100)
except KeyboardInterrupt:
    print "wtf"
    global exitnow
    exitnow = True
    sys.exit()
    
