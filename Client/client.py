#-------------------------------------------------------------------------------
# Instituto Tecnologico de Costa Rica-Area Academica Ingenieria en Computadores
# Principios de Sistemas Operativos - Tarea Corta 2 - Containers Jobs
# Estudiante-carnet: Giovanni Villalobos Quiros - 2013030976
# Based on code from - Basado en codigo tomado de
# https://stackoverflow.com/questions/42458475/sending-image-over-sockets-only-in-python-image-can-not-be-open
#-------------------------------------------------------------------------------

import random
import socket, select, os
from time import gmtime, strftime, sleep
from random import randint

HOST = '172.17.0.1'
PORT = 6666

#sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#server_address = (HOST, PORT)


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = (HOST, PORT)
sock.connect(server_address)
answer = sock.recv(4096)
if (answer == "Not Accepted"):
    print "Conexion Rechazada con Host"
else:
    print "Conexion Establecida con Host"

    while True:
        image = raw_input("Enter image name: ")
        file_extension = os.path.splitext(image)[1]

        if (image == "Salir"):
            print "Saliendo..."
            sock.sendall("BYE BYE ")
            sock.close()
            break

        myfile = open(image, 'rb')
        bytes = myfile.read()
        size = len(bytes)
        # send image size to server
        sock.sendall("SIZE %s" % size)
        answer = sock.recv(4096)

        print 'answer = %s' % answer

        if answer == 'GOT SIZE':
            # send extension to server
            sock.sendall("EXT %s" % file_extension)
            answer = sock.recv(4096)

        print 'answer = %s' % answer

        if answer == 'GOT EXT':
            # send data bytes to server
            print 'Sending Image to Server'
            sock.sendall(bytes)
            # check what server send
            answer = sock.recv(4096)
            print 'answer = %s' % answer

            if answer == 'GOT IMAGE' :
                print 'Image successfully send to server'

        myfile.close()
