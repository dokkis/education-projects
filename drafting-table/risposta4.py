# Gallo, Antonio, 406104

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from risposta3 import *

#PyPlaSM:
#def risposta4():
#    points = getCurvePoints(curvePoint1, curvePoint2, curvePoint3, 15)
#    l=[]
#    for p in points:
#        alphaRot, betaRot = alfabeta(p)
#        l.append(drawTecnigrafo(xArm, yArm, zArm, alphaRot, betaRot))
#        
#    VIEW(STRUCT(l))
    
def risposta4():
    """ Visualizza i bracci del tecnigrafo in 15 posizioni diverse sulla curva """
    points = pointsAndDrawCurve(15)
    for p in points:
        alphaRot, betaRot = alfabeta(p)
        drawTecnigrafo(xArm, yArm, zArm, alphaRot, betaRot, 1)    

view = (0.0, 0.0, 1.0, 0, 0.0, 0.0, 0.0, 1.0, 0.0)

def alfabeta(p):
    """ Ritorna il valore degli angoli di giunto in funzione della posizione del punto terminale lungo la curva """
    l1 = xArm-yArm
    l2 = l1
    l3 = sqrt( p[0]*p[0] + p[1]*p[1] )
     # se il punto e' in 0,0 le lunghezze sono nulle e ritorna 0 e 180
    if(l1!=0 and l2!=0 and l3!=0):  
    # Teorema di Carnot e uno sulle tangenti m=tgAlpha   
        m = p[1]/p[0]
        atn = degrees(atan(m))
        cosAlpha = (l1*l1 + l3*l3 - l2*l2)/(2*l1*l3)
        alpha = degrees( acos(cosAlpha) )
        
        cosBeta = (l1*l1 + l2*l2 - l3*l3)/(2*l1*l2)
        beta = degrees( acos(cosBeta) )
    
        alphaRot = atn-alpha
        betaRot = 180+alphaRot-beta        
    else:
        alphaRot = 0
        betaRot = 180
    
    return alphaRot, betaRot

def display(): 
    """ Callback di draw della finestra, viene visualizzata risposta2() che disegna tavolo e curva inclinati """  
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(*view)     
    
    risposta4() 

    glutSwapBuffers()
    
def reshape(w, h):
    """ Callback di ridimensionamento della finestra, ricalcola il volume di vista glOrtho in modo da avere una visualizzazione isomorfa della scena """
    if(w == 0): w = 1
    if(h == 0): h = 1  
    aspectRatio = float(w) / float(h) 
    if (w <= h): u,v = 1,1/aspectRatio
    else: u,v = aspectRatio, 1   
    
    orthoW1,orthoW2,orthoH1, orthoH2  = -4.0, 24.0, -12.0, 16.0
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()    
    glOrtho (orthoW1*u, orthoW2*u, orthoH1*v, orthoH2*v, -100.0, 100.0)    
    display()
    
if __name__ == '__main__':
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB| GLUT_DEPTH)
    glutInitWindowSize(600, 600)
    glutInitWindowPosition(100, 100)
    glutCreateWindow("Tecnigrafo")
    init()
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutMainLoop()

