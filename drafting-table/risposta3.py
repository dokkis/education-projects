# Gallo, Antonio, 406104

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from risposta2 import *
from math import *

xArm=(lunghezzaTavolo+altezzaTavolo)/2
yArm=1.
zArm=0.1

xSquad=5.
ySquad=0.5
zSquad=0.1

def risposta3():   
    """ Visualizza il tavolo ed il modello dei bracci con la squadretta alla fine """
    tavolo()
    glPushMatrix()
    t(yArm/2,0,yArm/2)
    t(lunghezzaTavolo/2, larghezzaTavolo*2.4, altezzaTavolo/2)
    r(-alphaTavolo, 1, 0, 0)
    t(-lunghezzaTavolo/2, 0, -altezzaTavolo/2)    
    t(0,zArm,0)  
    drawTecnigrafo(xArm, yArm, zArm, 0 , 20, 3) 
    glPopMatrix()  

view = (1.0, 1.0, 1.0, 0, 0.0, 0.0, 0.0, 1.0, 0.0)

#PyPlaSM:
#def armModel(xArm, yArm, zArm, angolo):  
#    arm = CUBOID([xArm, zArm, yArm])
#    arm = T([1,3])([-yArm/2, -yArm/2])(arm)
#    arm = R([1,3])(math.radians(angolo))(arm)
#    return SKELETON(1)(arm)

def armModel(xArm, yArm, zArm, angolo, width): 
    """ Visualizza un braccio dati in input le sue grandezze x, y, z e l'angolo di rotazione e lo spessore della linea di disegno """ 
    glPushMatrix()
    glLineWidth(width)
    r(angolo,0,0,1)
    t(xArm/2-yArm/2,0,0)
    glScale(xArm, yArm, zArm)    
    glutWireCube(1.0)
    glPopMatrix()

#PyPlaSM:
#def drawSquadre(alpha, beta):
#    s1 = armModel(xSquad, ySquad, zSquad, 0)
#    s2 = armModel(xSquad, ySquad, zSquad, 90)
#    t1 = T([1,3])([math.cos(math.radians(alpha))*(xArm-yArm), math.sin(math.radians(alpha))*(xArm-yArm)])
#    t2 = T([1,3])([math.cos(math.radians(beta))*(xArm-yArm), math.sin(math.radians(beta))*(xArm-yArm)])
#    return STRUCT([t1, t2, s1, s2])

def drawSquadre(alpha, beta, spessore):
    """ Visualizza la squadretta attaccate ai bracci opportunamente traslata """
    glPushMatrix()    
    t(cos(radians(beta))*(xArm-yArm),0, sin(radians(beta))*(xArm-yArm) )
    t(cos(radians(alpha))*(xArm-yArm),  0,sin(radians(alpha))*(xArm-yArm))
    armModel(xSquad, ySquad, zSquad, 0, spessore)
    armModel(xSquad, ySquad, zSquad, 90, spessore)
    glPopMatrix()
    
#PyPlaSM:
#def drawTecnigrafo(xArm, yArm, zArm, alpha, beta):
#    s= drawSquadre(alpha, beta)
#    a1=armModel(xArm, yArm, zArm, alpha)
#    a2=armModel(xArm, yArm, zArm, beta)
#    a2=T([1,3])([math.cos(math.radians(alpha))*(xArm-yArm), math.sin(math.radians(alpha))*(xArm-yArm)])(a2)
#    return STRUCT([s,a1,a2])

def drawTecnigrafo(xArm, yArm, zArm, alpha, beta, spessore):
    """ Visualizza il tecnigrafo composto dalle squadre e dai bracci """
    drawSquadre(alpha, beta, spessore)
    armModel(xArm, yArm, zArm, alpha, spessore)  
    glPushMatrix()
    t(cos(radians(alpha))*(xArm-yArm), 0, sin(radians(alpha))*(xArm-yArm))
    armModel(xArm, yArm, zArm, beta, spessore)
    glPopMatrix()
    
def display():   
    """ Callback di draw della finestra, viene visualizzata risposta2() che disegna tavolo e curva inclinati """
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)    
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(*view)         
    risposta3()              
    glutSwapBuffers()
    
def reshape(w, h):
    """ Callback di ridimensionamento della finestra, ricalcola il volume di vista glOrtho in modo da avere una visualizzazione isomorfa della scena """
    if(w == 0): w = 1
    if(h == 0): h = 1  
    aspectRatio = float(w) / float(h) 
    if (w <= h): u,v = 1,1/aspectRatio
    else: u,v = aspectRatio, 1       
    orthoW1,orthoW2,orthoH1, orthoH2  = -10.0, 18.0, -17.0, 11.0
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()    
    glOrtho (orthoW1*u, orthoW2*u, orthoH1*v, orthoH2*v, -100.0, 100.0)    
    display()
    
if __name__ == '__main__':
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB| GLUT_DEPTH)
    glutInitWindowSize(800, 600)
    glutInitWindowPosition(100, 100)
    glutCreateWindow("Tecnigrafo")
    init()
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutMainLoop()

