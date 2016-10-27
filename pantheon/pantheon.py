#!/usr/bin/env python
# -*- coding: utf-8 -*- 

# Gallo, Antonio, 406104

from pyplasm import *
# Grandezze relative al Pronao e all'AvanCorpo:
raggioColonna, altezzaColonna, distanzaColonne = 0.25, 4.5, 1.5
tettoX, tettoY, tettoZ = 11, 1, 9
altezzaCuspide = 4
lunghezzaAvancorpo, larghezzaAvancorpo, altezzaAvancorpo = tettoX, 4.2, 10
basePronaoAvancorpoX, basePronaoAvancorpoY, basePronaoAvancorpoZ= tettoX*1.2, altezzaAvancorpo/20., tettoZ*1.1
altezzaRilievi = altezzaAvancorpo/20.
# Grandezze relative al Cilindro Principale
altezzaCilindro = altezzaAvancorpo
raggioCilindroInterno, raggioCilindroEsterno = 8, 10
altezzaRilieviCorone = altezzaRilievi
# Grandezze relative alla Cupola
raggioColonneInterne = 0.25
altezzaColonneInterne = 3.5
altezzaCupola = 5.
altezzaRilieviCupola = altezzaCilindro/20.
taglioCupola = altezzaCilindro/33.
# Grandezze dei piccoli Tempi Interni
lunghezzaTempio = 1.5
larghezzaTempio = 0.4
altezzaTempio = altezzaColonneInterne*0.8
raggioColonneTempio = 0.15

#///////////// RISPOSTA 1 /////////////
def colonna(r, h):
    """ Restituisce una colonna di raggio r e altezza h composta da una base cuboide, una colonna cilindrica e un capitello cuboide """
    base = CUBOID([2*r*1.2, 2*r*1.2, h/12.])
    cil = CYLINDER( [r, (10./12)*h ] )(36)
    capitello = base
    return INSR(TOP)([base, cil, capitello])

def rigaColonne(n):
    """ rigaColonne(n)([t, r, h]) E' una funzione del secondo ordine.
    Restituisce una riga di n colonne parametrizzata rispetto una lista composta da un parametro traslazione (t), raggio (r) delle colonne e altezza (h) delle colonne"""
    def rigaColonne0(args):
        t, r, h = args
        col = colonna(r, h)
        return STRUCT([col, T(1)(t)] * n)
    return rigaColonne0

def cuspide3D(l, w, h):
    """ Restituisce una cuspide di lunghezza l, larghezza w e altezza h """
    cuspide = MKPOL([ [[l/2.,0,h/2.],[l/2.,w,h/2.]],[[1,2]],None ])
    basis = EMBED(1)(CUBOID([l, w]))
    return JOIN([basis, cuspide])

def cuspideBucata(l, w, h, scala, larghezzaInterna):
    """ Restituisce una cuspide incavata in una cuspide di un fattore di scala 'scala' e di larghezza larghezzaInterna applicando una trasformazione
    di scala con il tringaolo centrato negli assi di riferimento """
    cuspide = T([1,3])([-l/2. ,-h/4])(cuspide3D(l, w, h))                                      
    cuspideDiff3D = S([1,2,3])([scala,larghezzaInterna,scala])(cuspide)
    diff = DIFFERENCE([cuspide, cuspideDiff3D ])
    return T([1,3])([l/2. ,h/4])(diff)

def colonnatoPronao():
    """ Restituisce le 16 colonne del Pronao utilizzando colonna e rigaColonne opportunamente
    compone le prime 8 righe con una chiamata rigaColonne(8) e le altre 8 sono composte di rigaColonne(2) traslate opportunamente"""
    dueColonne = rigaColonne(2)([distanzaColonne*2, raggioColonna, altezzaColonna])    
    quattroColonne = STRUCT([dueColonne, T(1)(distanzaColonne*5)(dueColonne)])    
    primaRigaColonne = rigaColonne(8)([distanzaColonne, raggioColonna, altezzaColonna])
    secondaRigaColonne = T(2)(distanzaColonne)(quattroColonne)
    terzaRigaColonne = T(2)(distanzaColonne*2)(quattroColonne)    
    return STRUCT([ primaRigaColonne, secondaRigaColonne, terzaRigaColonne ])

def tettoPronao():
    """ Restituisce il tetto del Pronao composto da 5 cuboidi impilati uno sopra l'altro per avere degli effetti di rilievo con in testa una cuspide bucata """
    t1 = CUBOID([tettoX, tettoZ, tettoY*3./12])
    t2 = CUBOID([tettoX + 0.1, tettoZ + 0.1, tettoY*1./12])
    t3 = CUBOID([tettoX, tettoZ, tettoY*3./12])
    t4 = CUBOID([tettoX + 0.2, tettoZ + 0.2, tettoY*1./12])
    t5 = CUBOID([tettoX + 0.3, tettoZ + 0.3, tettoY*3./12])
    l,w,h = tettoX + 0.4, tettoZ + 0.4, altezzaCuspide
    cuspide = cuspideBucata(l, w, h, 0.8, 0.05)
    return INSL(TOP)([t1, t2, t3, t4, t5, cuspide])

def avancorpo():
    """ Restituisce l'avancorpo composto da un cuboide come base a cui vengono sottrati due cilindri, un cuboide per l'ingresso del pantheon e a cui
    vengono aggiunti dei cuboidi per i rilievi laterali che si congiungeranno con i rilievi del Cilindro Principale. Viene infine aggiunta una
    cuspide bucata per un ulteriore rilievo frontale """
    base = CUBOID([tettoX, larghezzaAvancorpo, altezzaAvancorpo ])
    cil = CYLINDER([ tettoX/11. , altezzaAvancorpo*0.4 ])(100)
    ingresso = CUBOID([tettoX/4., larghezzaAvancorpo, altezzaAvancorpo*0.4])
    ingresso = T(1)( tettoX/2. - tettoX/8.   )(ingresso)
    vx = 0.3
    rilievoBasso = T([1,3])([ -vx/2 , altezzaColonneInterne - altezzaRilievi])(CUBOID([tettoX + vx, larghezzaAvancorpo, altezzaRilievi]) )
    rilievoBasso = DIFFERENCE([rilievoBasso, ingresso])
    rilievoMedio = T([1,2,3])([ -vx/2 ,-0.2, altezzaColonneInterne*2 - altezzaRilievi])(CUBOID([tettoX + vx, larghezzaAvancorpo*1.1, altezzaRilievi]) )
    rilievoAlto = T([1,2,3])([ -vx/2 ,-0.2, altezzaCilindro - altezzaRilievi])(CUBOID([tettoX + vx, larghezzaAvancorpo*1.1, altezzaRilievi]) )
    cuspide = cuspideBucata(tettoX, larghezzaAvancorpo, altezzaCuspide, 0.8, 0.05)    
    cuspide = T([2, 3])([-0.2, altezzaColonneInterne*2 ] )(cuspide)
    base = STRUCT([base, rilievoMedio,rilievoBasso, rilievoAlto, cuspide])    
    return INSL(DIFFERENCE)([base, T(1)(tettoX/11*2)(cil), T(1)(tettoX/11*2 + tettoX/1.6)(cil), ingresso])  

def pronao():
    """ Restituisce il pronao come una struttura comprensiva di colonnato e tetto creati tramite colonnatoPronao() e tettoPronao (traslato in altezza) """
    colonnato = colonnatoPronao()
    tetto = tettoPronao()
    tetto = T(3)(altezzaColonna)(tetto)    
    return STRUCT([colonnato, tetto])

def risposta1():
    """ Restituisce e visualizza una struttura composta da avancorpo, pronao e una base sotto di essi opportunamente traslati """
    avanc = avancorpo()
    avanc = T(2)(tettoZ/1.8)(avanc)
    pron = pronao()
    base = CUBOID([basePronaoAvancorpoX, basePronaoAvancorpoZ, basePronaoAvancorpoY])
    assemblato = STRUCT([avanc, pron])
    assemblato = TOP([base, assemblato])                     
    assemblato = T([1, 2 ])([-(basePronaoAvancorpoX)/2, -(basePronaoAvancorpoZ)/2])(assemblato)
    VIEW( assemblato )
    return assemblato

#///////////// RISPOSTA 2 /////////////
def g(gradi):
    """ Funzione che trasforma i gradi in radianti tramite la proporzione (2*PI/360) * gradi """
    return (2*PI/360)*gradi

def circonferenza(R):
    """ Ritorna la funzione circonferenza0, utilizzata per realizzare una circonferenza """
    def circonferenza0(p):
        u = S1(p)
        return [R*COS(u), R*SIN(u)]
    return circonferenza0

def metaColonnato():
    """ Costruisce metà del Colonnato Interno tracciando su una circonferenza 6 punti ottenuti visualizzando lo 0-Scheletro di un opportuno QUOTE
    a cui viene applicato un MAP con la funzione circonferenza. Dai punti iterativamente tramite l'enumerazione con UKPOL vengono create, traslate
    e ruotate le colonne opportunamente """    
    dom = T(1)(-PI/2)(QUOTE( [-g(40), g(10), g(-35), g(10), g(-35), g(10), -g(40)]))
    out = SKEL_0( MAP(circonferenza( raggioCilindroInterno ) )( dom ) )
    points = UKPOL(out)[0]
    colList = []
    colRotation = [g(-45), g(-45), 0, 0, g(45), g(45)]
    for i in range (0,6):
        p = points[i]
        col = colonna(raggioColonneInterne, altezzaColonneInterne)
        col = T([1,2])([-2*raggioColonna*1.2, -2*raggioColonna*1.2])(col)
        col = R([1,2])(colRotation[i] )(col)
        colList.append( T([1,2])([p[0], p[1]])(col) )
    return STRUCT(colList)

def risposta2():
    """ Restituisce e visualizza l'intero colonnato interno come una struttura composta da colonnato1 costruito con metaColonnato() e da colonnato2
    ottenuto attraverso la rotazione di 180 gradi di colonnato2 """
    colonnato1 = metaColonnato()
    colonnato2 = R([1,2])(PI)(colonnato1)
    assemblato = STRUCT([colonnato1, colonnato2])    
    VIEW(assemblato)
    return assemblato

#///////////// RISPOSTA 3 /////////////
def cerchio(dom):
    """ Serve per realizzare un cerchio pieno """
    u, v, w = dom
    return [v*COS(u), v*SIN(u), w]

def corona(R, r, h):
    """ Serve per realizzare una corona circolare di raggio esterno R, raggio interno r e altezza h sfruttando la funzione cerchio """
    dom3d = INSL(PROD)( [INTERVALS(2*PI)(100), T(1)(r)(INTERVALS(R-r)(3)), INTERVALS(h)(1) ])
    cor = MAP(cerchio)(dom3d)
    return cor

def tempioInterno(l, w, h, r):
    """ Restituisce un piccolo tempio di lunghezza l, larghezza w, altezza h con raggio delle colonne h
    composto da una base, due colonne e una cuspide bucata """
    base = CUBOID([l, w, h*0.1])
    colonne = rigaColonne(2)([ (l - 2*r)*0.9  ,r, h*0.6])
    cuspide = cuspideBucata(l, w, h*0.3, 0.8, w*0.2)
    tempio = INSL(TOP)([base, colonne, cuspide])
    tempio = T([1,2])([-l/2., -w])(tempio)
    return tempio

def tempiInterni():
    """ Restituisce otto tempi disposti su una circonferenza distanziati di 45 gradi e opportunamente ruotati """
    dom = QUOTE( [g(45), g(-45)] * 2 )
    out = SKEL_0( MAP(circonferenza( raggioCilindroInterno ) )( dom ) )
    points = UKPOL(out)[0]
    tempiList = []
    tRotation = [ g(-90), g(-45), g(0), g(45) ]
    for i in range (0,4):
        p = points[i]
        tempio = tempioInterno(lunghezzaTempio,larghezzaTempio,altezzaTempio, raggioColonneTempio)
        tempio = R([1,2])(tRotation[i] )(tempio)
        tempiList.append( T([1,2])([p[0], p[1]])(tempio) )
    tempi = STRUCT(tempiList)
    return STRUCT([tempi, R([1,2])(PI)(tempi)])

def cilindroPrincipale():
    """ Restituisce la struttura del Cilindro Principale composta da 4 basse corone di rilievo e la corona principale opportunamente traslate.
    La struttura è sottratta ad un cuboide per realizzare l'ingresso del pantheon (leggermente più piccolo di quello dell'avancorpo) """
    coronaPrincipale = corona(raggioCilindroEsterno, raggioCilindroInterno, altezzaCilindro)
    coronaEsternaBase = corona(raggioCilindroEsterno*1.1, raggioCilindroInterno*1.1, altezzaRilieviCorone)
    coronaEsternaBassa = T(3)(altezzaColonneInterne)(corona(raggioCilindroEsterno*1.02, raggioCilindroInterno*0.9, altezzaRilieviCorone ) )
    coronaEsternaMedia = T(3)(altezzaColonneInterne*2)(corona(raggioCilindroEsterno*1.02, raggioCilindroInterno*0.9, altezzaRilieviCorone ) )
    coronaEsternaAlta = T(3)(altezzaCilindro)(corona(raggioCilindroEsterno*1.05, raggioCilindroInterno*0.9, altezzaRilieviCorone ) )
    tempi = R([1,2])(g(-23))(tempiInterni())    
    diffR = raggioCilindroEsterno-raggioCilindroInterno
    ingresso = T([1,2,3])([-((tettoX/4))/2,-diffR, altezzaRilieviCorone])(CUBOID([(tettoX/4), diffR*2,altezzaAvancorpo*0.4 ]))
    cilPrincipale = STRUCT([coronaPrincipale, coronaEsternaBassa])
    cilPrincipale = DIFFERENCE([cilPrincipale, T(2)(-(raggioCilindroInterno+diffR/2))(ingresso)])
    cilPrincipale = STRUCT([cilPrincipale, coronaEsternaBase, coronaEsternaMedia,coronaEsternaAlta, tempi, colonnatoInterno])
    return cilPrincipale
    
def risposta3():
    """ Restituisce e visualizza la struttura del Cilindro Principale """
    assemblato = cilindroPrincipale()
    VIEW(assemblato)
    return assemblato

#///////////// RISPOSTA 4 /////////////
def sfera(h):
    """ Serve per realizzare un solido sferico """
    def sfera0(point):
        u,v,z = point
        fx=z*SIN(u)*COS(v)
        fy=z*SIN(u)*SIN(v)
        fz=h*COS(u)
        return fx,fy,fz
    return sfera0

def cupola(R, r,h1, h2=0):
    """ Funzione che restituisce una cupola cava di raggio esterno R e raggio interno r, h1 è l'altezza della cupola, se h2 è maggiore di 0, la cupola
    sarà tagliata di h1-h2 """
    dom = INSL(PROD)([ T(1)(h2)(INTERVALS(PI/2.8-h2)(10)), INTERVALS(2*PI)(80), T(1)(r)(INTERVALS(R-r)(1)) ])
    return MAP( sfera(h1) )(dom)

def cupolaPantheon():
    """ Restituisce la cupola del pantheon composta da sette corone circolari impilate una sopra l'altra di raggio via via decrescente con in cima
    una cupola tagliata """
    corone = []
    scale1, scale2 = 0.95, 0.98
    coronaBase = corona(raggioCilindroEsterno*0.98, raggioCilindroInterno, altezzaRilieviCupola)
    corone.append(coronaBase)
    corone.append(T(3)(altezzaRilieviCupola))    

    for i in range(0,6):
        cor = corona(raggioCilindroEsterno*scale1, raggioCilindroInterno*scale2, taglioCupola)        
        corone.append(cor)
        corone.append(T(3)(taglioCupola))
        scale1=scale1-scale1/20
        scale2=scale2-scale2/20

    cupolaTagliata = cupola(raggioCilindroEsterno*scale1*1.1 , raggioCilindroEsterno*scale1*0.8, altezzaCupola, PI/2.5*0.2 )
    coroneStruct = STRUCT(corone)
    return INSL(TOP)([coroneStruct, cupolaTagliata])

def risposta4():
    """ Restituisce e visualizza la Cupola del Pantheon """
    assemblato = cupolaPantheon()
    VIEW(assemblato)
    return assemblato

#///////////// RISPOSTA 5 /////////////
def risposta5():
    """ Assembla tutti i modelli 3D di pronao, avancorpo, cilindro principale, cupola per ottenere il modello complessivo 3D del pantheon a cui viene
    applicata una semplice texture stile marmo e viene visualizzata """
    pantheon = STRUCT([ colonnatoInterno, cilindroPrincipale])
    pantheon = TOP([pantheon, cupola])
    pantheon = STRUCT([T(2)(-raggioCilindroEsterno-basePronaoAvancorpoZ*0.3)(pronaoEAvancorpo), pantheon])
    VIEW(pantheon)

pronaoEAvancorpo = risposta1()
colonnatoInterno = risposta2()
cilindroPrincipale = risposta3()
cupola = risposta4()
risposta5()
