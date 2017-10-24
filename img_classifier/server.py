#-------------------------------------------------------------------------------
# Instituto Tecnologico de Costa Rica-Area Academica Ingenieria en Computadores
# Principios de Sistemas Operativos - Tarea Corta 2 - Containers Jobs
# Estudiante-carnet: Giovanni Villalobos Quiros - 2013030976
# Based on code from - Basado en codigo tomado de
# https://stackoverflow.com/questions/42458475/sending-image-over-sockets-only-in-python-image-can-not-be-open
#-------------------------------------------------------------------------------

import parser as parserConfig
import random
import socket, select
from time import gmtime, strftime
from random import randint
import color_classifier
import netifaces as ni
import os

folderNameOriginal = "../carpetaDocker/containerRun"
folderNameNew = ""
imgcounter = 1
folderCounter = 0;
imgExtension = ".jpg"
foldersToCreate = ["R","G","B","Not_Trusted"]
connected_clients_sockets = []
server_socket = ""
notTrustedFolder = "/Not_Trusted"
HOST = "0.0.0.0"
PORT = 6666
buffer_size = 51200
notTrustedList, acceptedList  = parserConfig.parse()
print "Server Network info:"
#print os.system("ip addr | grep \'inet \'")
#print os.system("ifconfig | grep \'inet addr\' | cut -d: -f2 | awk \'{print $1}\'")
#Ips =  os.system("ifconfig | grep \'inet addr\' | cut -d: -f2 | awk \'{print $1}\'")
interfaces = ni.interfaces()
localAdresses = []
externalAdresses = []
#get all the possibles ips on the server
for inter in interfaces:
    if(("127" in ni.ifaddresses(inter)[ni.AF_INET][0]['addr'].split(".")) or ("172" in ni.ifaddresses(inter)[ni.AF_INET][0]['addr'].split("."))):
        localAdresses.append([inter + ":", ni.ifaddresses(inter)[ni.AF_INET][0]['addr']])
    else:
        externalAdresses.append([inter + ":", ni.ifaddresses(inter)[ni.AF_INET][0]['addr']])
#Print address for the user to be easier to get them
for addr in localAdresses:
    print "Posible Local Address:           ", "%8s" % addr[0], addr[1]
for addr in externalAdresses:
    print "Posible  External/Other Address: ", "%8s" % addr[0], addr[1]


#------------------------------------------------------------------------------
#----This function is in charge of the creation of the folders for the container
def createFolders():
    global folderCounter
    global folderNameNew
    folderNameNew = folderNameOriginal
    #Check if the folder container exists, if yes then appends a number from 1 to
    #infinite until a name is available
    while (os.path.exists(folderNameNew)):
        folderCounter = folderCounter + 1;
        folderNameNew = folderNameOriginal + str(folderCounter)
    #Create folder using the path of the original folder with the one
    #calculated above
    os.makedirs(folderNameNew)
    for folderN in foldersToCreate:
        #Creates a folder for each name in the list of foldersToCreate
        os.makedirs(folderNameNew + "/" + folderN)


#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
#----This function is in charge of the connection to the socket of the server

def connectSocket():
    global connected_clients_sockets, server_socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(10)
    connected_clients_sockets.append(server_socket)
    print("Started on port: " + str(PORT))


#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
#----This function is in charge of the receive image through socket to the server

def reciveImage(data, ip):
    global folderNameNew, imgExtension, imgcounter
    tempImgPath = folderNameNew + "/" + str(imgcounter) + imgExtension
    myfile = open(tempImgPath, 'wb')
    myfile.write(data)
    myfile.close()
    if not data:
        myfile.close()
        print "Not data in Image"
    elif ip in notTrustedList:
        print "Not trusted ip"
        newImagePathClassified = folderNameNew + notTrustedFolder + "/" + str(imgcounter) + imgExtension
    else:
        newImagePathClassified = folderNameNew + "/" + color_classifier.determine_predominant_color(tempImgPath) + "/" + str(imgcounter) + imgExtension
    #print "New path classified", newImagePathClassified
    #print "tempImgPath: ", tempImgPath
    os.rename(tempImgPath,newImagePathClassified)
    sock.send("GOT IMAGE")
    imgcounter += 1
#------------------------------------------------------------------------------
#----This function is in charge of the receive data through socket

def receiveFromSocket(sock):
    global imgExtension, buffer_size
    try:
        data = sock.recv(buffer_size)
        txt = str(data)

        if txt.startswith('SIZE'):
            tmp = txt.split()
            size = int(tmp[1])

            #print 'got size'
            #print 'size is %s' % size

            sock.send("GOT SIZE")

            buffer_size = 51200

        elif txt.startswith('EXT'):
            tmp = txt.split()
            imgExtension = tmp[1]
            sock.send("GOT EXT")
            # Now set the buffer size for the image
            buffer_size = 92160000

        elif txt.startswith('BYE'):
            #connected_clients_sockets.index(sockfd)
            print "Host %s Disconected" %  sockfd.getpeername()[0]
            sock.shutdown()

        elif data:
            print "--------------"
            print "Image Received"
            reciveImage(data, sock.getpeername()[0])
            buffer_size = 4096
            print "Image Processed"
    except:
        #print "Exception"
        sock.close()
        connected_clients_sockets.remove(sock)

createFolders()
connectSocket()

while True:

    read_sockets, write_sockets, error_sockets = select.select(connected_clients_sockets, [], [])

    for sock in read_sockets:

        if sock == server_socket:
            sockfd, client_address = server_socket.accept()
            print "Peername: " ,sockfd.getpeername()[0]
            if ((sockfd.getpeername()[0] in acceptedList) or (sockfd.getpeername()[0] in notTrustedList)):
                sockfd.send("Accepted")
                connected_clients_sockets.append(sockfd)
                print "Socket initializing with host %s" %  sockfd.getpeername()[0]
            else:
                sockfd.send("Not Accepted")
                sockfd.close()
                print "Ip not accepted"

        else:
            receiveFromSocket(sock)

server_socket.close()
