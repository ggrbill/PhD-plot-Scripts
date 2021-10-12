# -*- coding: cp1252 -*-
import numpy as np
import pylab as pl

pl.grid( True, which='both', axis='both', linestyle = '-', color = '#B5B5B5', linewidth=0.3 )
pl.xlim( 0.05, 0.3 )
pl.ylim( 0.1, 30. )
        

def getY( slope, x, b ):
    return 10**( slope*np.log10(x) + b )
'''
x1 e x2 são os extremos do triângulo.
yb é onde corta o eixo y. Isso controla a posição vertical do triângulo.
slope é a inclinação da reta. Deve ser 1.0 ou 2.0.
'''

def getUpperTri( x1, x2, yb, slope ):
    '''Constrói o triângulo pra ficar ACIMA das curvas (slope=1.0).'''
    X, Y = [], []
    X.append( [x1, x2] )
    X.append( [x2, x1] )
    X.append( [x1, x1] )
    y1 = getY( slope, x1, yb )
    y2 = getY( slope, x2, yb )
    Y.append( [y1, y2] )
    Y.append( [y2, y2] )
    Y.append( [y2, y1] )
    return X, Y

def getLowerTri( x1, x2, yb, slope ):
    '''Constrói o triângulo pra ficar ABAIXO das curvas (slope=2.0).'''
    X, Y = [], []
    X.append( [x1, x2] )
    X.append( [x2, x2] )
    X.append( [x2, x1] )
    y1 = getY( slope, x1, yb )
    y2 = getY( slope, x2, yb )
    Y.append( [y1, y2] )
    Y.append( [y2, y1] )
    Y.append( [y1, y1] )
    return X, Y


X1, Y1 = getUpperTri( 0.09, 0.14, 1.9, 1.0 )
X2, Y2 = getLowerTri( 0.11, 0.18, 1.35, 2.0 )


# Plota as retas dos triângulos
for x1, y1, x2, y2 in zip( X1, Y1, X2, Y2 ):
    pl.loglog( x1, y1, '-', color='grey' )
    pl.loglog( x2, y2, '-', color='grey' )



# tu é a posição do texto no Triângulo Upper
# tl é a posição do texto no Triângulo Lower
tu_x1, tu_y1 = 0.081, 8.2
tu_x2, tu_y2 = 0.102, 11.96
tl_x1, tl_y1 = 0.184, 0.376
tl_x2, tl_y2 = 0.140, 0.216

# Coloca os números nos triângulos
pl.text( tu_x1, tu_y1, '1.0' )
pl.text( tu_x2, tu_y2, '1.0' )
pl.text( tl_x1, tl_y1, '1.0' )
pl.text( tl_x2, tl_y2, '2.0' )

pl.xlabel( r'h - control volume size', size=14 )
pl.ylabel( r'Pressure error', size=14 )

pl.show()





