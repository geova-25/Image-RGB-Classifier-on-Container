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

#------------------------------------------------------------------------------
#----Some local variables

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
MAX_CONS = 50
buffer_size = 51200

#------------------------------------------------------------------------------
#----Get the data from the config file using the parser.py file imported

notTrustedList, acceptedList  = parserConfig.parse()

#------------------------------------------------------------------------------
#----This function is in charge of showing the network info to make easy to get ip

def showNetworkInfo():
    print "Server Network info:"
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
    print "-----------Server Started-----------------"


#------------------------------------------------------------------------------
#----This function is in charge of the creation of the folders for the container
def createFolders():
    #Use of global variables
    global folderCounter
    global folderNameNew
    #Using the global variable of the folder name defined above
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
    #global variabes for sockets
    global connected_clients_sockets, server_socket, maxCons
    #Uses the function of socket to start it
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #The server binds to the Host and Port defined above
    server_socket.bind((HOST, PORT))
    #The socket listen to maximum number of conection defined above in global
    server_socket.listen(MAX_CONS)
    #A list of the connected sockets available to make ir more accesible
    connected_clients_sockets.append(server_socket)
    print("Using port: " + str(PORT))


#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
#----This function is in charge of the receive image through socket to the server

def reciveImage(data, ip):
    global folderNameNew, imgExtension, imgcounter
    #The original path of where the image will be received and adds the image
    #counter and the extension of the image that was received from the client
    tempImgPath = folderNameNew + "/" + str(imgcounter) + imgExtension
    #Create a file using the path defined above
    myfile = open(tempImgPath, 'wb')
    #Write the data of the received image because the file color_classifier needs
    #the image to be stored
    myfile.write(data)
    #Close the file
    myfile.close()
    #If no data available
    if not data:
        myfile.close()
        print "Not data in Image"
    #If the Ip is not trusted
    elif ip in notTrustedList:
        print "Not trusted ip"
        #Makes a new path in the folder of Not_Trusted
        newImagePathClassified = folderNameNew + notTrustedFolder + "/" + str(imgcounter) + imgExtension
    else:
        #Creates a new path using the color_classifier import that tell where
        #the image shoul be stores if R, G or B
        newImagePathClassified = folderNameNew + "/" + color_classifier.determine_predominant_color(tempImgPath) + "/" + str(imgcounter) + imgExtension
    #The image previously saved is changed of location
    os.rename(tempImgPath,newImagePathClassified)
    sock.send("GOT IMAGE")
    imgcounter += 1
#------------------------------------------------------------------------------
#----This function is in charge of the receive data through socket

def receiveFromSocket(sock):
    global imgExtension, buffer_size
    #If there are available data and not error occured
    try:
        #Obtains data from buffer of socket
        data = sock.recv(buffer_size)
        #Makes it string to check for Instrucctions
        txt = str(data)
        #If the string is Size
        if txt.startswith('SIZE'):
            tmp = txt.split()
            #Save the size of the incomming image
            size = int(tmp[1])
            #Notify the client that image size was received
            sock.send("GOT SIZE")

            buffer_size = 51200
        #If the string is EXT
        elif txt.startswith('EXT'):
            tmp = txt.split()
            #Save the image extension comming from the client
            imgExtension = tmp[1]
            #Notify the client that image was received
            sock.send("GOT EXT")
            # Now set the buffer size for the image
            buffer_size = 92160000
        #If the connection closes
        elif txt.startswith('BYE'):
            print "Host %s Disconected" %  sockfd.getpeername()[0]
            #shutdown to block the connection to client of socket
            sock.shutdown()
        #When if the data of the image
        elif data:
            print "--------------"
            print "Image Received"
            #Call function received image
            reciveImage(data, sock.getpeername()[0])
            buffer_size = 4096
            print "Image Processed"
    except:
        #In error close the socket or call it after Bye to destroy it
        sock.close()
        #Eliminated from the list of clients sockets
        connected_clients_sockets.remove(sock)

createFolders()
connectSocket()
showNetworkInfo()

#Check always incomming sockets connections
while True:
    #Makes the waitable objects sockets return in a list to know which of them are ready
    #to be read, write or are error or exeption at the moment, in this case
    #only ready to read
    read_sockets, write_sockets, error_sockets = select.select(connected_clients_sockets, [], [])

    for sock in read_sockets:
        #If the socket is the server means a new connection is ready
        if sock == server_socket:
            #First it is accepted and then rejected or not, this because
            #is need to be connected to reach the ip info
            sockfd, client_address = server_socket.accept()
            #If it is in the list of accepted or not trusted keeps the connection
            if ((sockfd.getpeername()[0] in acceptedList) or (sockfd.getpeername()[0] in notTrustedList)):
                sockfd.send("Accepted")
                connected_clients_sockets.append(sockfd)
                print "Socket initializing with host %s" %  sockfd.getpeername()[0]
            #If not in any list then it is rejected
            else:
                sockfd.send("Not Accepted")
                sockfd.close()
                print "Ip not accepted"
        #If it is other socket it means incomming info
        else:
            receiveFromSocket(sock)
#close server at the end
server_socket.close()
