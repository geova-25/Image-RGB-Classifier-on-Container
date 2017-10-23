#-------------------------------------------------------------------------------
# Instituto Tecnologico de Costa Rica-Area Academica Ingenieria en Computadores
# Principios de Sistemas Operativos - Tarea Corta 2 - Containers Jobs
# Estudiante-carnet: Giovanni Villalobos Quiros - 2013030976
# Based on code from - Basado en codigo tomado de
# https://github.com/fengsp/color-thief-py
#-------------------------------------------------------------------------------

from colorthief import ColorThief

def determine_predominant_color(name):
    color_thief = ColorThief(name)
    # get the dominant color 1 for the quickest but lower accuracy
    dominant_color_tuple = color_thief.get_color(quality=1)
    dominant_color_value = max(dominant_color_tuple)
    dominant_color_index = dominant_color_tuple.index(dominant_color_value)
    if(dominant_color_index == 0):
        dominant_color_name = "red"
    elif(dominant_color_index == 1):
        dominant_color_name = "green"
    else:
        dominant_color_name = "blue"
    print "dominant_color_tuple", dominant_color_tuple
    print "dominant_color_value", dominant_color_value
    return dominant_color_name

img_name = 'saiyayin.jpg'
dominant_color_name = determine_predominant_color(img_name)
print "dominant_color_name", dominant_color_name
