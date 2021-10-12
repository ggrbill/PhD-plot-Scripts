# -*- coding: cp1252 -*-
"""
Created on Sun Jan 25 18:32:50 2015

@author: ggrbill
"""
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import ReadEFVLibInspectorFile as reader

color_list = [  '#4F81BD', '#C0504D', '#9BBB59', '#8064A2', '#1F497D', '#F79646', '#953735', '#4F6228', '#984807' 
    , '#4F81BD', '#C0504D', '#9BBB59', '#8064A2', '#1F497D', '#F79646', '#953735', '#4F6228', '#984807'
    , '#4F81BD', '#C0504D', '#9BBB59', '#8064A2', '#1F497D', '#F79646', '#953735', '#4F6228', '#984807' ]

## Lendo dados dos Arquivos
nDiv = 6
numberOfCurves = 10
timeLevels = [1,5,10,20,40]  #,400,600,1000,1500,2000,3500]
numberOfCurves = len( timeLevels )
vDispFile = reader.ReadEFVLibInspectorFile("AppGeomechanics2D_test//topDisplacement_603.csv", nDiv, timeLevels)

currentTime = vDispFile.getCurrentTime()
vDisplacement = vDispFile.getVariableData()
xValues = vDispFile.getXAxisValues()

vDispFile.reorderData( xValues )

# Changing the Units (Pa->kPa, m->mm)  
# Computing Total Stress
for i in range ( vDispFile.getNumberOfPlottingCurves() ):
    vDisplacement[i] = vDisplacement[i]*1000

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
for i in range(numberOfCurves):
    plt.plot( xValues, vDisplacement[i], '-', color = color_list[i], linewidth = 1.2, label = str( currentTime[i]) )
   
## Mudando a posição e tamanho da área de plotagem
#box = axis.get_position()
#axis.set_position([box.x0-0.03, box.y0+0.03, box.width*0.7, box.height])

## linhas de grade posicionadas atrás das curvas plotadas
axis.set_axisbelow( True )
## Invertendo direção do Eixo X
#axis.invert_xaxis()
#
### Tamanho da fonte dos "labels" dos marcadores (ticks)
plt.tick_params( axis='both', which='major', labelsize=12) 

### Limites dos eixos
xMin, xMax = plt.xlim()
plt.xlim( 0.0, xMax )
yMin, yMax = plt.ylim()
plt.ylim( -0.2, 0.8 )

### Configurando a legenda e os "labels" dos eixos - - -  bbox_to_anchor = (1.05, 0.5)
#plt.legend(loc = "center left", bbox_to_anchor = (1.05, 0.5), numpoints = 1, fontsize = 12, frameon=False, title=r"\bf{Time(s)}" )
#plt.legend(loc = "upper left", numpoints = 1, fontsize = 12, frameon=False, title=r"\bf{Time levels}" )
plt.ylabel( r" Vertical displacement (mm)", size = 16)
plt.xlabel( r" x(m) ", size = 16) 

###plt.savefig('C:\\Users\\ggrbill\\Desktop\\figure1.pdf')
plt.show()