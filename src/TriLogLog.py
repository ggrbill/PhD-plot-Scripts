# -*- coding: cp1252 -*-

def getUpperTri( x0, y0, l, slope ):
    '''Constrói o triângulo pra ficar ACIMA das curvas (slope=1.0).'''
    x1 = (x0 + l)
    x2 = x0
    y1 = ( y0 + ( slope*l ) )
    y2 = ( y0 + ( slope*l ) )
    xa = x0 + ( ((x1-x2)/2.0) - 0.1*l )
    ya = ( y0 + slope*l + 0.05)
    xb = ( x0 - 0.1 )
    yb = y0 + ( ( (y2-y0) / 2.0) - 0.05*slope*l )
    X, Y = [], []
    X.append( [10**(x0), 10**(x1)] )
    X.append( [10**(x1), 10**(x2)] )
    X.append( [10**(x2), 10**(x0)] )
    Y.append( [10**(y0), 10**(y1)] )
    Y.append( [10**(y1), 10**(y2)] )
    Y.append( [10**(y2), 10**(y0)] )
    Xa = 10**xa
    Ya = 10**ya
    Xb = 10**xb
    Yb = 10**yb
    return X, Y, Xa, Ya, Xb, Yb 

def getLowerTri( x0, y0, l, slope, p0 = 0.1 ):
    '''Constrói o triângulo pra ficar ABAIXO das curvas (slope=2.0).'''
    x1 = x0 + l 
    x2 = x0 + l 
    y1 = y0
    y2 = y0 + ( slope*l )
    xa = x0 + ( ((x1-x0)/2.0) - 0.1*l )
    ya = (y0 - p0)
    xb = ( x0 + l + 0.05 )
    yb = y0 + ( ( (y2-y1) / 2.0) - 0.15*slope*l )
    X, Y = [], []
    X.append( [10**x0, 10**x1] )
    X.append( [10**x1, 10**x2] )
    X.append( [10**x2, 10**x0] )
    Y.append( [10**y0, 10**y1] )
    Y.append( [10**y1, 10**y2] )
    Y.append( [10**y2, 10**y0] )
    Xa = 10**xa
    Ya = 10**ya
    Xb = 10**xb
    Yb = 10**yb
    return X, Y, Xa, Ya, Xb, Yb 

if __name__ == '__main__':

    import pylab as pl
    
    pl.figure(figsize=(8,6))
    pl.grid( True, which='both', axis='both', linestyle = '-', color = '#B5B5B5', linewidth=0.3 )
    #pl.xlim( 0.05, 0.3 )
    #pl.ylim( 0.1, 30. )
    pl.xlim( 1.0e-2, 1.0e0 )
    pl.ylim( 1.0e-2, 1.0e0 )
    
    #X1, Y1 = getUpperTri( 0.09, 0.14, 1.9, 1.0 )
    #X2, Y2 = getLowerTri( 0.11, 0.18, 1.35, 2.0 )
    XU, YU, tu_x1, tu_y1, tu_x2, tu_y2 = getUpperTri( -1.8, -1, 0.4, 1.0 )
    XL, YL, tl_x1, tl_y1, tl_x2, tl_y2 = getLowerTri( -1.7, -1.7, 0.3, 2.0 )
    
    # Plota as retas dos triângulos
    for x1, y1, x2, y2 in zip( XL, YL, XU, YU ):
        pl.loglog( x1, y1, '-', color='grey' )
        pl.loglog( x2, y2, '-', color='grey' )
    
    # tu é a posição do texto no Triângulo Upper
    # tl é a posição do texto no Triângulo Lower
    #tu_x1, tu_y1 = 0.11, 0.22
    #tu_x2, tu_y2 = 0.07, 0.14
#    tl_x1, tl_y1 = 0.029, 0.015
#    tl_x2, tl_y2 = 0.058, 0.036
    
    # Coloca os números nos triângulos
    pl.text( tu_x1, tu_y1, '1.0' )
    pl.text( tu_x2, tu_y2, '1.0' )
    pl.text( tl_x1, tl_y1, '1.0' )
    pl.text( tl_x2, tl_y2, '2.0' )
    
    pl.xlabel( r'h - control volume size', size=14 )
    pl.ylabel( r'Pressure error', size=14 )
    
    pl.show()