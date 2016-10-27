# Gallo, Antonio, 406104

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from risposta4 import *

msAnimation = 5

def risposta5():
    """ Visualizza il tavolo ed il tecnigrafo """
    tavolo()    
    tecnigrafo()

def tecnigrafo():
    """ Visualizza il tecnigrafo con opportune rotazioni e traslazioni """
    global points, alpha, beta
    glPushMatrix()
    t(yArm/2,0,yArm/2)
    t(lunghezzaTavolo/2, larghezzaTavolo*2.4, altezzaTavolo/2)
    r(-alphaTavolo, 1, 0, 0)
    t(-lunghezzaTavolo/2, 0, -altezzaTavolo/2)    
    points = drawCurve([2,altezzaTavolo/3,0], [lunghezzaTavolo/2,altezzaTavolo/1.1,0], [lunghezzaTavolo/1.2,altezzaTavolo/4,0], 50)  
    p = points[i]     
    alpha, beta = alfabeta(p)
    glPushMatrix()  
    t(0,zArm,0)  
    drawTecnigrafo(xArm, yArm, zArm, alpha, beta, 3)
    glPopMatrix()
    glPopMatrix()   

view = (1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

def display():
    """ Callback di draw della finestra, viene visualizzata risposta2() che disegna tavolo e curva inclinati """  
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(*view)    
   
    risposta5() 
    
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
    
i, pos = 0, 1
alpha, beta= 0, 0

def animate(value):
    """ Viene richiamato da un timer ogni msAnimation millisecondi, cambia ad ogni tick il punto su cui il tecnigrafo deve puntare le sue squadrette """
    global i, points, pos

    if(pos==1):
        i=i+1
        if(i>=len(points)-1):
            pos = -1
        glutPostRedisplay()
    else:
        i=i-1
        if(i<=0):
            pos = 1
        glutPostRedisplay()
    
    display()
    
    glutTimerFunc(msAnimation, animate, 1)
    
    
if __name__ == '__main__':
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB| GLUT_DEPTH)
    glutInitWindowSize(800, 600)
    glutInitWindowPosition(100, 100)
    glutCreateWindow("Tecnigrafo")
    init()
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glClearColor(0.3,0.4,0.5,1)
    #l'amimazione parte dopo x msec
    x=100
    glutTimerFunc(x, animate, 1)
    glutMainLoop()

