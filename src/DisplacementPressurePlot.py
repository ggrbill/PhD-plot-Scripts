# -*- coding: cp1252 -*-
"""
Created on Sun Jan 25 18:32:50 2015

@author: ggrbill
"""
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import TerzaghisProblemAnalytical as analytical

#t = open("Terzaghi_6_Dt_0_1_EbFVM//topDisplacement_306.csv")
#b = open("Terzaghi_6_Dt_0_1_EbFVM//BottomPressure_306.csv")
#s = open("Terzaghi_6_Dt_0_1_EbFVM//BottomSigmaYY_306.csv")

grid = "91"
dt = "1"
t = open("Terzaghi_6_Convergence//Conv_Terzaghi_6_Dt_"+ dt +"_EBFVM//topDisplacement_"+ grid +".csv")
b = open("Terzaghi_6_Convergence//Conv_Terzaghi_6_Dt_"+ dt +"_EBFVM//BottomPressure_"+ grid +".csv")
s = open("Terzaghi_6_Convergence//Conv_Terzaghi_6_Dt_"+ dt +"_EBFVM//BottomSigmaYY_"+ grid +".csv")

nDiv = 6;

tList = ( t ).readlines();
numberOfLines = len( tList ) - 3;
bList = ( b ).readlines();
numberOfPoints = int(numberOfLines/nDiv);
sList = ( s ).readlines();

currentTime = []
anlCurrentTime = []
topDisplacement = []
anlDisplacement = []
bottomPressure = []
anlPressure = []
bottomStress = []
totalStress = []

#for i in range(numberOfLines):
#    anlCurrentTime.append( float( tList[i+3].split(',')[0] ) )
#    
#anlCurrentTime = np.array(anlCurrentTime)

TopStress = 1.0e+6 # Pa
for i in range(numberOfPoints):
    pointIndex = i*nDiv;
    currentTime.append( float( tList[pointIndex+3].split(',')[0] ) )
    topDisplacement.append( float( tList[pointIndex+3].split(',')[1] )*1000 )
    pressure = float( bList[pointIndex+3].split(',')[1] ) /1000
    stress = float( sList[pointIndex+3].split(',')[1] )*(-1.0) / 1000
    bottomPressure.append( pressure  )
    bottomStress.append( stress )
#    totalStress.append( pressure+stress )
    totalStress.append( TopStress/1000 )
    
t.close()
b.close()
s.close()
currentTime = np.array(currentTime)
topDisplacement = np.array(topDisplacement)
bottomPressure = np.array(bottomPressure)
bottomStress = np.array(bottomStress)
totalStress = np.array(totalStress)


## calculando a solução analitica
N = 200
#                                   height, tao_0, permeability, phi, mi, K, K_s, K_f, G, K_phi 
#o = analytical.TerzaghisProblemAnalytical( 6.0, TopStress , 1.9e-15, 0.19, 0.001, 8.0e+9, 3.6e+10, 3.3e+9, 6.0e+9, 3.6e+10 )
o = analytical.TerzaghisProblemAnalytical( 6.0, TopStress , 1.9e-15, 0.19, 0.001, 8.0e+9, 3.6e+10, 3.3e+9, 6.0e+9, 3.6e+10 )
anlCurrentTime = o.getTimeValues( currentTime[-1] )
anlCurrentTime = np.array(anlCurrentTime)

anlDisplacement = o.getDisplacementValuesConstPosition( 6.0, currentTime[-1] )
anlPressure = o.getPressureValuesConstPosition( 0.0, currentTime[-1] )

#for i in range(numberOfLines):
#    anlDisplacement.append( o.getDisplacementValue( 6.0, anlCurrentTime[i], N )*1000 )
#    anlPressure.append( o.getPressureValue( 0.0, anlCurrentTime[i], N )/1000 )
    
anlDisplacement = np.array(anlDisplacement)
anlPressure = np.array(anlPressure)
anlDisplacement = 1000*anlDisplacement
anlPressure = anlPressure/1000

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
plt.plot( anlCurrentTime, anlDisplacement, '-', linewidth = 0.9, color = '#9BBB59', label = r"Anal\'{\i}tica")
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
plt.ylabel( r" Deslocamento(mm)", size = 16)
plt.xlabel( r" Tempo(s) ", size = 16) 

##plt.savefig('C:\\Users\\ggrbill\\Desktop\\figure2.pdf')
plt.show()

## Criando o gráfico
fig = plt.figure( num = 2, figsize = (7,5) )
axis = plt.subplot(111)

## Plotando dados (função loglog) e linhas de grade (função grid)
plt.grid( True, which='both', axis='both', linestyle = '-', color = '#B5B5B5' )
plt.plot( anlCurrentTime, anlPressure, '-', linewidth = 0.9, color = '#9BBB59', label = r"Anal\'{\i}tica")
plt.plot( currentTime, bottomPressure, 'o', markersize = 4, color = '#9BBB59', markeredgecolor = '#9BBB59', label = r"Num\'erica")

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
fig = plt.figure( num = 3, figsize = (7,5) )
axis = plt.subplot(111)

## Plotando dados (função loglog) e linhas de grade (função grid)
plt.grid( True, which='both', axis='both', linestyle = '-', color = '#B5B5B5' )
plt.plot( currentTime, totalStress, 'o-', linewidth = 1.0, color = 'black', markersize = 4, label = r"Tens\~ao total")
plt.plot( currentTime, bottomStress, 'o-', linewidth = 1.0, color = '#4F81BD', markeredgecolor = '#4F81BD', markersize = 4, label = r"Tens\~ao efetiva")
plt.plot( currentTime, bottomPressure, 'o-', linewidth = 1.0, color = '#C0504D', markeredgecolor = '#C0504D', markersize = 4, label = r"Press\~ao")

## Mudando a posição e tamanho da área de plotagem
#box = axis.get_position()
#axis.set_position([box.x0-0.03, box.y0+0.03, box.width*0.7, box.height])

## linhas de grade posicionadas atrás das curvas plotadas
axis.set_axisbelow( True )

## Tamanho da fonte dos "labels" dos marcadores (ticks)
plt.tick_params( axis='both', which='major', labelsize=12)

### Limites dos eixos
xMin, xMax = plt.xlim()
plt.xlim( 0.0, xMax )
yMin, yMax = plt.ylim()
plt.ylim( 0.0, 1050 ) 

## Configurando a legenda e os "labels" dos eixos
plt.legend(loc = "center right", numpoints = 1, fontsize = 12, frameon=True, fancybox=True, borderpad=1, labelspacing=0.5)  # labelspacing, title=r"\bf{Total stress}" )
plt.ylabel( r" Tens\~ao/Press\~ao(kPa)", size = 16)
plt.xlabel( r" Tempo(s) ", size = 16) 

