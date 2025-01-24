from .vars import *
def setcatname(name):
    global catname
    catname=name
def getcatname():
    global catname
    return catname
def setcatoptions(one):
    global catoptions
    catoptions["one"]=one
def getcatoptions():
    global catoptions
    return f"Color: {catoptions["one"]}"

        
        