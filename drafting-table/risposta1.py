# Gallo, Antonio, 406104

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

# Grandezze
altezzaTavolo = 12.
lunghezzaTavolo = 20.
larghezzaTavolo = 0.5

larghezzaSupporto=larghezzaTavolo*2

distanzaSostegni=lunghezzaTavolo/8
lunghezzaSostegni=lunghezzaTavolo/20

altezzaSostegni=altezzaTavolo
larghezzaPiede=lunghezzaTavolo/2

# Rotazione tavolo 
alphaTavolo = 30

#Non serve poiche le rotazioni in OpenGL sono in gradi
#def g(angolo):
#    return angolo*2*PI/360

#PyPLASM:
#def risposta1():
#    VIEW(tavolo(30))

def risposta1():
    """ Visualizza la risposta1 """
    tavolo()

def cuboid(x, z, y):
    """ Visualizza un CUBOID di grandezze x, y, z centrato nel punto in basso a sinistra """
    glPushMatrix()    
    glScalef(x, y, z)    
    glTranslatef(0.5, 0.5, 0.5)     
    glColor3f(1.0, 1.0, 1.0)
    glutSolidCube(1.0)   
    glPopMatrix()

def t(x, z, y):
    """ Definisce una glTraslatef(x,y,z) """
    glTranslatef(x,y,z)
    
def r(gradi, x, y, z):
    """ Definisce una glRotatef(gradi, x, y, z) """
    glRotatef(gradi, x, y, z)
    
#PyPLASM:
#def tavolo(alpha):
#    base = baseTavolo()
#    tavolo = CUBOID([lunghezzaTavolo, larghezzaTavolo, altezzaTavolo])
#    tavolo = T([1,3])([-lunghezzaTavolo/2, -altezzaTavolo/2])(tavolo)
#    tavolo = R([2,3])(g(alpha))(tavolo)
#    tavolo = T([1,2,3])([lunghezzaTavolo/2, larghezzaTavolo, altezzaTavolo/2])(tavolo)
#    return STRUCT([tavolo, base])
#

def tavolo():
    """ Visualizza il tavolo comprensivo di base di appoggio (baseTavolo) """
    #baseTavolo
    baseTavolo()
    #tavolo
    glPushMatrix()
    t(lunghezzaTavolo/2, larghezzaTavolo, altezzaTavolo/2)
    r(-alphaTavolo, 1, 0, 0)
    t(-lunghezzaTavolo/2, 0, -altezzaTavolo/2)
    cuboid(lunghezzaTavolo, larghezzaTavolo, altezzaTavolo)
    glPopMatrix()
    
#PyPLASM:
#def baseTavolo():
#    base = CUBOID([lunghezzaTavolo, altezzaTavolo, larghezzaTavolo/4])
#    base = T([2,3])([-altezzaTavolo/2,-altezzaSostegni])(base)
#    supporto = CUBOID([lunghezzaTavolo, larghezzaSupporto, larghezzaSupporto ])
#    sostegno = CUBOID([lunghezzaSostegni, larghezzaSupporto, altezzaSostegni])
#    piede = CUBOID([lunghezzaSostegni, larghezzaPiede, altezzaSostegni])
#    sostegno1 = T([1,3])([distanzaSostegni,-altezzaSostegni])(sostegno)
#    sostegno2 = T([1,3])([lunghezzaTavolo-distanzaSostegni-lunghezzaSostegni, -altezzaSostegni])(sostegno)
#    return STRUCT([T(3)(altezzaTavolo/2 - larghezzaSupporto),base, supporto, sostegno1, sostegno2])

def baseTavolo():  
    """ Visualizza la base del tavolo """  
    glPushMatrix()
    t(0,0, altezzaTavolo/2 - larghezzaSupporto)
    #base
    glPushMatrix()
    t(0, -altezzaTavolo/2,-altezzaSostegni -larghezzaTavolo/2)
    cuboid(lunghezzaTavolo, altezzaTavolo, larghezzaTavolo/2)
    glPopMatrix()
    #supporto
    cuboid(lunghezzaTavolo, larghezzaSupporto, larghezzaSupporto)
    #sostegno1
    glPushMatrix()
    t(distanzaSostegni, 0, -altezzaSostegni)
    cuboid(lunghezzaSostegni, larghezzaSupporto, altezzaSostegni)
    glPopMatrix()
    #sostegno2
    glPushMatrix()
    t(lunghezzaTavolo-distanzaSostegni-lunghezzaSostegni, 0, -altezzaSostegni)
    cuboid(lunghezzaSostegni, larghezzaSupporto, altezzaSostegni)
    glPopMatrix()
    glPopMatrix()

def initLight():
   ambient =  0.0, 0.0, 0.0, 1.0 
   diffuse =  1.0, 1.0, 1.0, 1.0 
   specular =  0.0, 1.0, 1.0, 1.0 
   position =  10, 25.0, 30.0, 0.1
   lmodel_ambient =  0.4, 0.4, 0.4, 1.0 
   local_view =  0.0

   glShadeModel(GL_SMOOTH)

   glLightfv(GL_LIGHT0, GL_AMBIENT, ambient)
   glLightfv(GL_LIGHT0, GL_DIFFUSE, diffuse)
   glLightfv(GL_LIGHT0, GL_POSITION, position)
   glLightModelfv(GL_LIGHT_MODEL_AMBIENT, lmodel_ambient)
   glLightModelfv(GL_LIGHT_MODEL_LOCAL_VIEWER, local_view)

   glEnable(GL_LIGHTING)
   glEnable(GL_LIGHT0)

def init():
    """ Inizializza l'ambiente OpenGL (e' presente solo qui poiche' tutti i file utilizzano risposta1) """
    glClearColor(0.0, 0.0, 0.0, 0.0)    
    glShadeModel(GL_FLAT)
    glEnable(GL_DEPTH_TEST)
    initLight()

view = (1.0, 1.0, 1.0, 0, 0.0, 0.0, 0.0, 1.0, 0.0)

def display():   
    """ Callback di draw della finestra, viene visualizzata risposta1(), ovvero il tavolo """
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(*view)  

    risposta1()
    
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

