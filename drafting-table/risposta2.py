# Gallo, Antonio, 406104

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from risposta1 import *

# Tre punti della curva in funzione della grandezza del tavolo
curvePoint1 = [2,altezzaTavolo/3,0]
curvePoint2 = [lunghezzaTavolo/2,altezzaTavolo/1.1,0]
curvePoint3 = [lunghezzaTavolo/1.2,altezzaTavolo/4,0]

def risposta2():
    """ Visualizza il tavolo e la curva a schermo che viene opportunamente traslata e ruotata per avere la stessa inclinazione del tavolo """
    glPushMatrix()
    t(lunghezzaTavolo/2, larghezzaTavolo*2.4, altezzaTavolo/2)
    r(-alphaTavolo, 1, 0, 0)
    t(-lunghezzaTavolo/2, 0, -altezzaTavolo/2)    
    glColor3f(1.0,0.0,0.0)
    pointsAndDrawCurve(15)
    glColor3f(1.0,0.0,0.0)
    glPopMatrix()    
    tavolo()
    
def pointsAndDrawCurve(n):
    """ Visualizza una curva polinomiale di secondo grado e restituisce n campioni equidistanti della curva (la curva viene definita con tre punti di controllo poiche la curva e' di secondo grado) """
    points = drawCurve(curvePoint1, curvePoint2, curvePoint3, n)  
    return points

def drawCurvePoints(points):
    """ Dati i punti della curva disegna polilinee prendendo i punti della curva due a due (point[i] e point[i+1]) """
    glDisable(GL_LIGHTING)    
    glPushMatrix() 
    glColor3f(1.0,0.0,0.0)
    glLineWidth(1.5); 
    glBegin(GL_LINES); 
    for i in range(len(points)-1):
        p1 = points[i]
        p2 = points[i+1]                    
        glVertex3f(p1[0], p1[1], p1[2])
        glVertex3f(p2[0], p2[1], p2[2])              
    glEnd();
    glLineWidth(1)
    glPopMatrix()
    glEnable(GL_LIGHTING)   


def lagrange2grado(u, p1, p2, p3):
    """ Dati tre punti della curva, restituisce il punto che appartiene alla curva con u dato """
    a = 2*u*u - 3*u + 1
    b = -4*u*u + 4*u
    c = 2*u*u - u        
    return [ a*p1[0] + b*p2[0] + c*p3[0], a*p1[1] + b*p2[1] + c*p3[1], a*p1[2] + b*p2[2] + c*p3[2] ]

def interval(A,N):
    """ Divide un intervallo A in N parti. Es: interval(1,4) = [0.0, 0.25, 0.5, 0.75, 1.0] """
    return [float(A)/float(N)*i for i in range(N+1)]

def getCurvePoints(p1, p2, p3, campioni):
    """ Restituisce i punti di una curva dati 3 punti di controllo ed il numero di campioni"""
    intervallo = interval(1, campioni)    
    points = map(lambda u: lagrange2grado(u, p1, p2, p3), intervallo )
    return points

def drawCurve(p1, p2, p3, campioni):
    """ Visualizza una curva dati suoi 3 punti ed il numero di campioni con cui disegnarla, maggiori sono i campioni piu e' definita la curva """
    points = getCurvePoints(p1, p2, p3, campioni)
    drawCurvePoints(points)
    return points
    
view = (1.0, 1.0, 1.0, 0, 0.0, 0.0, 0.0, 1.0, 0.0)

def display():   
    """ Callback di draw della finestra, viene visualizzata risposta2() che disegna tavolo e curva inclinati """
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(*view)
 
    risposta2()
        
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

