# -*- coding: cp1252 -*-
"""
Created on Sun Jan 25 18:32:50 2015

@author: ggrbill
"""
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import MandelsProblemAnalytical as analytical

plt.close('all')

#u = open("Mandel_2_dt_0_1_FEM//rightDisplacement_603.csv")
#t = open("Mandel_2_dt_0_1_FEM//topDisplacement_603.csv")
#b = open("Mandel_2_dt_0_1_FEM//PressureLeft_603.csv")
#s = open("Mandel_2_dt_0_1_FEM//SigmaYYLeft_603.csv")

dt = "1"
grid = "228"

u = open("Mandel_2_Convergence//Mandel_2_Dt_" + dt + "_EbFVM//rightDisplacement_" + grid + ".csv")
t = open("Mandel_2_Convergence//Mandel_2_Dt_" + dt + "_EbFVM//topDisplacement_" + grid + ".csv")
b = open("Mandel_2_Convergence//Mandel_2_Dt_" + dt + "_EbFVM//PressureLeft_" + grid + ".csv")
s = open("Mandel_2_Convergence//Mandel_2_Dt_" + dt + "_EbFVM//SigmaYYLeft_" + grid + ".csv")

nDiv = 6;

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

biot = 0.77777777777777777777777777777777777777777777777777777777777777777777777
for i in range(numberOfPoints):
    pointIndex = i*nDiv;
    currentTime.append( float( tList[pointIndex+3].split(',')[0] ) )
    topDisplacement.append( float( tList[pointIndex+3].split(',')[1] )*1000000 )
    rightDisplacement.append( float( uList[pointIndex+3].split(',')[1] )*1000000 )
    pressure = float( bList[pointIndex+3].split(',')[1] ) /1000
    stress = float( sList[pointIndex+3].split(',')[1] )*(-1.0) / 1000
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
    anlRightDisplacement.append( o.getHorDisplacementValue( 10.0, anlCurrentTime[i], N )*1000000 )  
    anlPressure.append( o.getPressureValue( 0.0, anlCurrentTime[i], N )/1000 )
    anlStress.append( -o.getVertStressValue( 0.0, anlCurrentTime[i], N )/1000 )
    
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
fig = plt.figure( num = 1, figsize = (7,5) )
axis = plt.subplot(111)

## Plotando dados (função loglog) e linhas de grade (função grid)
plt.grid( True, which='both', axis='both', linestyle = '-', color = '#B5B5B5' )
plt.plot( anlCurrentTime, anlTopDisplacement, '-', linewidth = 0.9, color = '#9BBB59', label = r"Anal\'{\i}tica")
plt.plot( currentTime, topDisplacement, 'o', color = '#9BBB59',  markersize = 4, markeredgecolor = '#9BBB59', label = r"Num\'erica")

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
plt.legend(loc = "lower right", numpoints = 1, fontsize = 12, frameon=True, fancybox=True, borderpad=1, labelspacing=0.5 )
plt.ylabel( r"Deslocamento vertical($\mu$m)", size = 16)
plt.xlabel( r" Tempo(s) ", size = 16) 

##plt.savefig('C:\\Users\\ggrbill\\Desktop\\figure2.pdf')
plt.show()


## Criando o gráfico
fig = plt.figure( num = 2, figsize = (7,5) )
axis = plt.subplot(111)

## Plotando dados (função loglog) e linhas de grade (função grid)
plt.grid( True, which='both', axis='both', linestyle = '-', color = '#B5B5B5' )
plt.plot( anlCurrentTime, anlRightDisplacement, '-', linewidth = 0.9, color = '#9BBB59', label = r"Anal\'{\i}tica")
plt.plot( currentTime, rightDisplacement, 'o', color = '#9BBB59',  markersize = 4, markeredgecolor = '#9BBB59', label = r"Num\'erica")

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
plt.legend(loc = "upper right", numpoints = 1, fontsize = 12, frameon=True, fancybox=True, borderpad=1, labelspacing=0.5 )
plt.ylabel( r" Deslocamento horizontal($\mu$m)", size = 16)
plt.xlabel( r" Tempo(s) ", size = 16) 

##plt.savefig('C:\\Users\\ggrbill\\Desktop\\figure2.pdf')
plt.show()

# Criando o gráfico
fig = plt.figure( num = 3, figsize = (7,5) )
axis = plt.subplot(111)

## Plotando dados (função loglog) e linhas de grade (função grid)
plt.grid( True, which='both', axis='both', linestyle = '-', color = '#B5B5B5' )
plt.plot( anlCurrentTime, anlPressure, '-', linewidth = 0.9, color = '#9BBB59', label =  r"Anal\'{\i}tica")
plt.plot( currentTime, pressureLeft, 'o', markersize = 4, color = '#9BBB59', markeredgecolor = '#9BBB59', label = r"Num\'erica")

## Mudando a posição e tamanho da área de plotagem
#box = axis.get_position()
#axis.set_position([box.x0-0.03, box.y0+0.03, box.width*0.7, box.height])

## linhas de grade posicionadas atrás das curvas plotadas
axis.set_axisbelow( True )

## Tamanho da fonte dos "labels" dos marcadores (ticks)
plt.tick_params( axis='both', which='major', labelsize=12) 

## Configurando a legenda e os "labels" dos eixos
plt.legend(loc = "upper right", numpoints = 1, fontsize = 12, frameon=True, fancybox=True, borderpad=1, labelspacing=0.5 )
plt.ylabel( r" Press\~ao(kPa)", size = 16)
plt.xlabel( r" Tempo(s) ", size = 16) 

##plt.savefig('C:\\Users\\ggrbill\\Desktop\\figure2.pdf')
plt.show()

## Criando o gráfico
fig = plt.figure( num = 4, figsize = (7,5) )
axis = plt.subplot(111)

## Plotando dados (função loglog) e linhas de grade (função grid)
plt.grid( True, which='both', axis='both', linestyle = '-', color = '#B5B5B5' )
plt.plot( anlCurrentTime, anlStress, '-', linewidth = 0.9, color = '#9BBB59', label = r"Anal\'{\i}tica")
plt.plot( currentTime, stressLeft, 'o', markersize = 4, color = '#9BBB59', markeredgecolor = '#9BBB59', label = r"Num\'erica")

## Mudando a posição e tamanho da área de plotagem
#box = axis.get_position()
#axis.set_position([box.x0-0.03, box.y0+0.03, box.width*0.7, box.height])

## linhas de grade posicionadas atrás das curvas plotadas
axis.set_axisbelow( True )

## Tamanho da fonte dos "labels" dos marcadores (ticks)
plt.tick_params( axis='both', which='major', labelsize=12) 

## Configurando a legenda e os "labels" dos eixos
plt.legend(loc = "upper right", numpoints = 1, fontsize = 12, frameon=True, fancybox=True, borderpad=1, labelspacing=0.5  )
plt.ylabel( r" Tens\~ao vertical total (kPa)", size = 16)
plt.xlabel( r" Tempo(s) ", size = 16) 

