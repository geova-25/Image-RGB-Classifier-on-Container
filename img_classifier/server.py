import random
import socket, select
from time import gmtime, strftime
from random import randint
import color_classifier
import os

folderNameOriginal = "../carpetaDocker/containerRun"
folderNameNew = ""
imgcounter = 1
folderCounter = 0;
imgExtension = ".jpg"
foldersToCreate = ["R","G","B","Not trusted"]
connected_clients_sockets = []
HOST = '0.0.0.0'
PORT = 6666
buffer_size = 51200

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
    global connected_clients_sockets
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(10)
    connected_clients_sockets.append(server_socket)
    print("Started on port: " + str(PORT))


#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
#----This function is in charge of the send of data through socket to the server




createFolders()
connectSocket()

while True:

    read_sockets, write_sockets, error_sockets = select.select(connected_clients_sockets, [], [])

    for sock in read_sockets:

        if sock == server_socket:

            sockfd, client_address = server_socket.accept()
            connected_clients_sockets.append(sockfd)

        else:
            try:
                print ' Buffer size is %s' % buffer_size
                data = sock.recv(buffer_size)
                txt = str(data)

                if txt.startswith('SIZE'):
                    tmp = txt.split()
                    size = int(tmp[1])

                    print 'got size'
                    print 'size is %s' % size

                    sock.send("GOT SIZE")

                    buffer_size = 51200

                elif txt.startswith('EXT'):
                    tmp = txt.split()
                    imgExtension = tmp[1]
                    sock.send("GOT EXT")
                    # Now set the buffer size for the image
                    buffer_size = 40960000

                elif txt.startswith('BYE'):
                    sock.shutdown()

                elif data:
                    tempImgPath = folderNameNew + "/" + str(imgcounter) + imgExtension
                    myfile = open(tempImgPath, 'wb')
                    # data = sock.recv(buffer_size)
                    if not data:
                        myfile.close()
                        print "Not data in Image"
                        break
                    myfile.write(data)
                    myfile.close()
                    newImagePathClassified = folderNameNew + "/" + color_classifier.determine_predominant_color(tempImgPath) + "/" + str(imgcounter) + imgExtension
                    print "New path classified", newImagePathClassified
                    print "tempImgPath: ", tempImgPath
                    os.rename(tempImgPath,newImagePathClassified)
                    #myfile = open(folderNameNew + "/" + folderNameNewColor + "/" + str(imgcounter) + imgExtension , 'wb')
                    sock.send("GOT IMAGE")
                    imgcounter += 1
                    buffer_size = 4096
                    sock.shutdown()
            except:
                sock.close()
                connected_clients_sockets.remove(sock)
                continue

server_socket.close()
