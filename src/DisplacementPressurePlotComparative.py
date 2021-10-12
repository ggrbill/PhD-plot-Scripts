# -*- coding: cp1252 -*-
"""
Created on Sun Jan 25 18:32:50 2015

@author: ggrbill
"""
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import TerzaghisProblemAnalytical as analytical

t = open("Terzaghi_6_Dt_0_1_EBFVM//topDisplacement_602.csv")
b = open("Terzaghi_6_Dt_0_1_EBFVM//BottomPressure_602.csv")

t1 = open("Terzaghi_2Regions_0_Rk_10_EBFVM//topDisplacement_602.csv")
b1 = open("Terzaghi_2Regions_0_Rk_10_EBFVM//BottomPressure_602.csv")

t2 = open("Terzaghi_2Regions_3_Dif_Mec_EBFVM//topDisplacement_602.csv")
b2 = open("Terzaghi_2Regions_3_Dif_Mec_EBFVM//BottomPressure_602.csv")

nDiv = 1;

tList = ( t ).readlines();
bList = ( b ).readlines();

tList1 = ( t1 ).readlines();
bList1 = ( b1 ).readlines();

tList2 = ( t2 ).readlines();
bList2 = ( b2 ).readlines();

numberOfLines = len( tList1 ) - 3;
numberOfPoints = int(numberOfLines/nDiv);

currentTime = []
topDisplacement = []
bottomPressure = []
topDisplacement1 = []
bottomPressure1 = []
topDisplacement2 = []
bottomPressure2 = []

TopStress = 1.0e+6 # Pa
for i in range(numberOfPoints):
    pointIndex = i*nDiv;
    currentTime.append( float( tList[pointIndex+3].split(',')[0] ) )
    topDisplacement.append( float( tList[pointIndex+3].split(',')[1] )*1000 )
    bottomPressure.append( float( bList[pointIndex+3].split(',')[1] ) /1000 )
    topDisplacement1.append( float( tList1[pointIndex+3].split(',')[1] )*1000 )
    bottomPressure1.append( float( bList1[pointIndex+3].split(',')[1] ) /1000 )
    topDisplacement2.append( float( tList2[pointIndex+3].split(',')[1] )*1000 )
    bottomPressure2.append( float( bList2[pointIndex+3].split(',')[1] ) /1000 )
    
t.close()
b.close()
t1.close()
b1.close()
t2.close()
b2.close()

currentTime = np.array(currentTime)
topDisplacement = np.array(topDisplacement)
bottomPressure = np.array(bottomPressure)
topDisplacement1 = np.array(topDisplacement1)
bottomPressure1 = np.array(bottomPressure1)
topDisplacement2 = np.array(topDisplacement2)
bottomPressure2 = np.array(bottomPressure2)

## Lista de Cores
color_list = [  '#4F81BD', '#9BBB59', '#F79646' ]
lineWidth = 1.2

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
fig = plt.figure( num = 1, figsize = (10,6) )
axis = plt.subplot(111)

## Plotando dados (função loglog) e linhas de grade (função grid)
plt.grid( True, which='both', axis='both', linestyle = '-', color = '#B5B5B5' )
plt.plot( currentTime, topDisplacement , '-', color = color_list[0], linewidth = lineWidth, label = 'Single Column')
plt.plot( currentTime, topDisplacement1, '-', color = color_list[1], linewidth = lineWidth, label = 'Double Column - Two Permeabilities')
plt.plot( currentTime, topDisplacement2, '-', color = color_list[2], linewidth = lineWidth, label = 'Double Column - Two Materials')

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
plt.legend(loc = "center right", numpoints = 1, fontsize = 12, frameon=True, title=r"\bf{Vertical displacement}" )
plt.ylabel( r" Displacement(mm)", size = 16)
plt.xlabel( r" Time(s) ", size = 16) 

##plt.savefig('C:\\Users\\ggrbill\\Desktop\\figure2.pdf')
plt.show()

## Criando o gráfico
fig = plt.figure( num = 2, figsize = (10,6) )
axis = plt.subplot(111)

## Plotando dados (função loglog) e linhas de grade (função grid)
plt.grid( True, which='both', axis='both', linestyle = '-', color = '#B5B5B5' )
plt.plot( currentTime, bottomPressure , '-', color = color_list[0], linewidth = lineWidth, label = 'Single Column')
plt.plot( currentTime, bottomPressure1, '-', color = color_list[1], linewidth = lineWidth, label = 'Double Column - Two Permeabilities')
plt.plot( currentTime, bottomPressure2, '-', color = color_list[2], linewidth = lineWidth, label = 'Double Column - Two Materials')

## Mudando a posição e tamanho da área de plotagem
#box = axis.get_position()
#axis.set_position([box.x0-0.03, box.y0+0.03, box.width*0.7, box.height])

## linhas de grade posicionadas atrás das curvas plotadas
axis.set_axisbelow( True )

## Tamanho da fonte dos "labels" dos marcadores (ticks)
plt.tick_params( axis='both', which='major', labelsize=12) 

## Configurando a legenda e os "labels" dos eixos
plt.legend(loc = "upper right", numpoints = 1, fontsize = 12, frameon=True, title=r"\bf{Pressure}" )
plt.ylabel( r" Pressure(kPa)", size = 16)
plt.xlabel( r" Time(s) ", size = 16) 

##plt.savefig('C:\\Users\\ggrbill\\Desktop\\figure2.pdf')
plt.show()
