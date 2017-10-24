#-------------------------------------------------------------------------------
# Instituto Tecnologico de Costa Rica-Area Academica Ingenieria en Computadores
# Principios de Sistemas Operativos - Tarea Corta 2 - Containers Jobs
# Estudiante-carnet: Giovanni Villalobos Quiros - 2013030976
#-------------------------------------------------------------------------------

def getIpList(configFile):
    f = open(configFile,"r")
    listNotTrusted = []
    listAccepted = []
    if(f.readline() == "Accepted:\n"):
        for line in f:
            if (line == "Not Trusted:\n"):
                break
            else:
                listAccepted.append(line.splitlines()[0])
        for line in f:
            listNotTrusted.append(line.splitlines()[0])
    return listNotTrusted, listAccepted
    #print "listNotTrusted: ", listNotTrusted
    #print "listAccepted:   " , listAccepted

def parse():
        return getIpList("../carpetaDocker/configuracion.config")
