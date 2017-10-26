#-------------------------------------------------------------------------------
# Instituto Tecnologico de Costa Rica-Area Academica Ingenieria en Computadores
# Principios de Sistemas Operativos - Tarea Corta 2 - Containers Jobs
# Estudiante-carnet: Giovanni Villalobos Quiros - 2013030976
# Based on code from - Basado en codigo tomado de
# https://stackoverflow.com/questions/42458475/sending-image-over-sockets-only-in-python-image-can-not-be-open
#-------------------------------------------------------------------------------

import random
import socket, select, os, sys
from time import gmtime, strftime, sleep
from random import randint

#-------------------------------------------------------------------------------
#-----------------------------Info to connect to the server

PORT = 6666
#Info of the ip is get dinamically
HOST = os.path.basename(sys.argv[1])

#-------------------------------------------------------------------------------
#-----------------------------Socket connection to the server
#INitializates the socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#Makes a tuple of server address and port
server_address = (HOST, PORT)
#Connect to that address and port
sock.connect(server_address)
#Waits for the answer of the server if it is or not an accepted request
answer = sock.recv(4096)

#-------------------------------------------------------------------------------
#-----------------------------If not accepted then ends

if (answer == "Not Accepted"):
    print "Rejected Connection with Server of ip: %s"  % sock.getpeername()[0]

#-----------------------------Else a loop is create to start sending the images

else:
    print "Stablished Conection with Server of ip: %s" % sock.getpeername()[0]
    while True:
        #Get the image path to send
        image = raw_input("Enter image path: ")
        #get the path of the image and get the extention of it
        file_extension = os.path.splitext(image)[1]
        #If the user inputs = Salir then it closes and end
        if (image == "Salir"):
            #Send the server the signal to close this connection
            sock.sendall("BYE BYE ")
            #Close the socket
            sock.close()
            #Break loop
            break
        #If the socket is not closed or error is given then
        try:
            #Open the file with that name or path
            myfile = open(image, 'rb')
            #Read the bytes of the image
            bytes = myfile.read()
            #Get the size of it
            size = len(bytes)
            #Send image size to server
            sock.sendall("SIZE %s" % size)
            #Waits for aswer of server
            answer = sock.recv(4096)
        #In case that that name did not exist then initial part of the loop if reach
        except:
            print "File does not exist, try again with the right path"
            continue

        #If the server responds that got the size
        if answer == 'GOT SIZE':
            #Send extension to server
            sock.sendall("EXT %s" % file_extension)
            #Waits for confirmation of server
            answer = sock.recv(4096)
        #If the server responds that got the extention then
        if answer == 'GOT EXT':
            #Send data bytes to server
            print 'Sending Image to Server'
            sock.sendall(bytes)
            #Waits and check what server send
            answer = sock.recv(4096)
            #If finally the server responds that the image was correctly received then
            if answer == 'GOT IMAGE' :
                print 'Image successfully sent'
        #Close the file
        myfile.close()
