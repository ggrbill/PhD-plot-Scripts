# -*- coding: cp1252 -*-
"""
Created on Sun Jan 25 18:32:50 2015

@author: ggrbill
"""
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import MandelsProblemAnalytical as analytical

u = open("Mandel_Solution_57_Elements//rightDisplacement_57.csv")
t = open("Mandel_Solution_57_Elements//topDisplacement_57.csv")
b = open("Mandel_Solution_57_Elements//PressureLeft_57.csv")
s = open("Mandel_Solution_57_Elements//SigmaYYLeft_57.csv")

nDiv = 8;

tList = ( t ).readlines();
numberOfLines = len( tList ) - 3;
numberOfPoints = int(numberOfLines/nDiv);
bList = ( b ).readlines();
sList = ( s ).readlines();
uList = ( u ).readlines();

currentTime = []
anlCurrentTime = []
topDisplacement = []
anlTopDisplacement = []
rightDisplacement = []
anlRightDisplacement = []
pressureLeft = []
anlPressure = []
stressLeft = []
anlStress = []

for i in range(numberOfLines):
    anlCurrentTime.append( float( tList[i+3].split(',')[0] ) )
    
anlCurrentTime = np.array(anlCurrentTime)

biot = 0.7777777777777777778
for i in range(numberOfPoints):
    pointIndex = i*nDiv;
    currentTime.append( float( tList[pointIndex+3].split(',')[0] ) )
    topDisplacement.append( float( tList[pointIndex+3].split(',')[1] )*1000000 )
    rightDisplacement.append( float( uList[pointIndex+3].split(',')[1] )*1000 )
    pressure = float( bList[pointIndex+3].split(',')[1] ) 
    stress = float( sList[pointIndex+3].split(',')[1] )*(-1.0)
    pressureLeft.append( pressure  )
    stressLeft.append( stress + biot*pressure )

u.close()    
t.close()
b.close()
s.close()
currentTime = np.array(currentTime)
topDisplacement = np.array(topDisplacement)
rightDisplacement = np.array(rightDisplacement)
pressureLeft = np.array(pressureLeft)
stressLeft = np.array(stressLeft)

## calculando a solução analitica
N = 200
# lenght, height, F, permeability, phi, mi, K, K_s, K_f, G, K_phi 
o = analytical.MandelsProblemAnalytical( 10.0, 2.0, 1.0e+4, 1.9e-15, 0.19, 0.001, 8.0e+9, 3.6e+10, 3.3e+9, 6.0e+9, 3.6e+10 )
for i in range(numberOfLines):
    anlTopDisplacement.append( o.getVertDisplacementValue( 2.0, anlCurrentTime[i], N )*1000000 )
    anlRightDisplacement.append( o.getHorDisplacementValue( 10.0, anlCurrentTime[i], N )*1000 )  
    anlPressure.append( o.getPressureValue( 0.0, anlCurrentTime[i], N ) )
    anlStress.append( -o.getVertStressValue( 0.0, anlCurrentTime[i], N ) )
    
anlTopDisplacement = np.array(anlTopDisplacement)
anlRightDisplacement = np.array(anlRightDisplacement)
anlPressure = np.array(anlPressure)
anlStress = np.array(anlStress)

## Mudando configurações padrões da borda do gráfico e das linhas de marcadores dos eixos (ticks markers)
matplotlib.rc('axes' ,edgecolor='#4F4F4F', linewidth = 1.5)
matplotlib.rcParams['xtick.major.size'] = 0
matplotlib.rcParams['xtick.minor.size'] = 0
matplotlib.rcParams['ytick.major.size'] = 0
matplotlib.rcParams['ytick.minor.size'] = 0

## Usando fontes do Latex
matplotlib.rc('font',**{'family':'serif','serif':['charter']})
matplotlib.rc('text', usetex=True)

## Criando o gráfico
fig = plt.figure( num = 1, figsize = (8,6) )
axis = plt.subplot(111)

## Plotando dados (função loglog) e linhas de grade (função grid)
plt.grid( True, which='both', axis='both', linestyle = '-', color = '#B5B5B5' )
plt.plot( anlCurrentTime, anlTopDisplacement, '-', linewidth = 0.9, color = 'black', label = 'Analytical')
plt.plot( currentTime, topDisplacement, 'o', color = 'black',  markersize = 4, markerfacecolor='none', markeredgecolor = 'black', label = 'Numerical')

## Mudando a posição e tamanho da área de plotagem
#box = axis.get_position()
#axis.set_position([box.x0-0.03, box.y0+0.03, box.width*0.7, box.height])

## linhas de grade posicionadas atrás das curvas plotadas
axis.set_axisbelow( True )
## Invertendo direção do Eixo Y
axis.invert_yaxis()

## Tamanho da fonte dos "labels" dos marcadores (ticks)
plt.tick_params( axis='both', which='major', labelsize=12) 

## Configurando a legenda e os "labels" dos eixos - - -  bbox_to_anchor = (1.05, 0.5)
plt.legend(loc = "lower right", numpoints = 1, fontsize = 12, frameon=True )
plt.ylabel( r"Vertical displacement ($\mu$m)", size = 16)
plt.xlabel( r" Time(s) ", size = 16) 

##plt.savefig('C:\\Users\\ggrbill\\Desktop\\figure2.pdf')
plt.show()


## Criando o gráfico
fig = plt.figure( num = 2, figsize = (8,6) )
axis = plt.subplot(111)

## Plotando dados (função loglog) e linhas de grade (função grid)
plt.grid( True, which='both', axis='both', linestyle = '-', color = '#B5B5B5' )
plt.plot( anlCurrentTime, anlRightDisplacement, '-', linewidth = 0.9, color = 'black', label = 'Analytical')
plt.plot( currentTime, rightDisplacement, 'o', color = 'black',  markersize = 4, markerfacecolor='none', markeredgecolor = 'black', label = 'Numerical')

## Mudando a posição e tamanho da área de plotagem
#box = axis.get_position()
#axis.set_position([box.x0-0.03, box.y0+0.03, box.width*0.7, box.height])

## linhas de grade posicionadas atrás das curvas plotadas
axis.set_axisbelow( True )
## Invertendo direção do Eixo Y
#axis.invert_yaxis()

## Tamanho da fonte dos "labels" dos marcadores (ticks)
plt.tick_params( axis='both', which='major', labelsize=12) 

## Configurando a legenda e os "labels" dos eixos - - -  bbox_to_anchor = (1.05, 0.5)
plt.legend(loc = "upper right", numpoints = 1, fontsize = 12, frameon=True )
plt.ylabel( r" Horizontal displacement (mm)", size = 16)
plt.xlabel( r" Time(s) ", size = 16) 

##plt.savefig('C:\\Users\\ggrbill\\Desktop\\figure2.pdf')
plt.show()

# Criando o gráfico
fig = plt.figure( num = 3, figsize = (8,6) )
axis = plt.subplot(111)

## Plotando dados (função loglog) e linhas de grade (função grid)
plt.grid( True, which='both', axis='both', linestyle = '-', color = '#B5B5B5' )
plt.plot( anlCurrentTime, anlPressure, '-', linewidth = 0.9, color = 'black', label = 'Analytical')
plt.plot( currentTime, pressureLeft, 'o', markersize = 4, markerfacecolor='none', color = 'black', markeredgecolor = 'black', label = 'Numerical')

## Mudando a posição e tamanho da área de plotagem
#box = axis.get_position()
#axis.set_position([box.x0-0.03, box.y0+0.03, box.width*0.7, box.height])

## linhas de grade posicionadas atrás das curvas plotadas
axis.set_axisbelow( True )

## Tamanho da fonte dos "labels" dos marcadores (ticks)
plt.tick_params( axis='both', which='major', labelsize=12) 

## Configurando a legenda e os "labels" dos eixos
plt.legend(loc = "upper right", numpoints = 1, fontsize = 12, frameon=True )
plt.ylabel( r" Pressure(Pa)", size = 16)
plt.xlabel( r" Time(s) ", size = 16) 

##plt.savefig('C:\\Users\\ggrbill\\Desktop\\figure2.pdf')
plt.show()

## Criando o gráfico
fig = plt.figure( num = 4, figsize = (8,6) )
axis = plt.subplot(111)

## Plotando dados (função loglog) e linhas de grade (função grid)
plt.grid( True, which='both', axis='both', linestyle = '-', color = '#B5B5B5' )
plt.plot( anlCurrentTime, anlStress, '-', linewidth = 0.9, color = 'black', label = 'Analytical')
plt.plot( currentTime, stressLeft, 'o', markersize = 4, markerfacecolor='none', color = 'black', markeredgecolor = 'black', label = 'Numerical')

## Mudando a posição e tamanho da área de plotagem
#box = axis.get_position()
#axis.set_position([box.x0-0.03, box.y0+0.03, box.width*0.7, box.height])

## linhas de grade posicionadas atrás das curvas plotadas
axis.set_axisbelow( True )

## Tamanho da fonte dos "labels" dos marcadores (ticks)
plt.tick_params( axis='both', which='major', labelsize=12) 

## Configurando a legenda e os "labels" dos eixos
plt.legend(loc = "upper right", numpoints = 1, fontsize = 12, frameon=True )
plt.ylabel( r" Vertical total stress (Pa)", size = 16)
plt.xlabel( r" Time(s) ", size = 16) 

