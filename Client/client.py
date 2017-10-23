#-------------------------------------------------------------------------------
# Instituto Tecnologico de Costa Rica-Area Academica Ingenieria en Computadores
# Principios de Sistemas Operativos - Tarea Corta 2 - Containers Jobs
# Estudiante-carnet: Giovanni Villalobos Quiros - 2013030976
# Based on code from - Basado en codigo tomado de
# https://stackoverflow.com/questions/42458475/sending-image-over-sockets-only-in-python-image-can-not-be-open
#-------------------------------------------------------------------------------

import random
import socket, select, os
from time import gmtime, strftime
from random import randint


image = raw_input("Enter image name: ")
file_extension = os.path.splitext(image)[1]

HOST = '172.17.0.1'
PORT = 6666

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = (HOST, PORT)
sock.connect(server_address)

try:

    # open image
    myfile = open(image, 'rb')
    bytes = myfile.read()
    size = len(bytes)

    # send image size to server
    sock.sendall("SIZE %s" % size)
    answer = sock.recv(4096)

    print 'answer = %s' % answer

    if answer == 'GOT SIZE':
        sock.sendall("EXT %s" % file_extension)
        answer = sock.recv(4096)

    print 'answer = %s' % answer

    # send image to server
    if answer == 'GOT EXT':
        sock.sendall(bytes)

        # check what server send
        answer = sock.recv(4096)
        print 'answer = %s' % answer

        if answer == 'GOT IMAGE' :
            sock.sendall("BYE BYE ")
            print 'Image successfully send to server'

    myfile.close()

finally:
    sock.close()
