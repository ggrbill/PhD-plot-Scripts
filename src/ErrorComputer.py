# -*- coding: cp1252 -*-
"""
Created on Sun Jan 25 18:32:50 2015

@author: ggrbill
"""
import numpy as np
import math
import matplotlib
import matplotlib.pyplot as plt
import TerzaghisProblemAnalytical as analytical
import ReadEFVLibInspectorFile as reader

color_list = [  '#4F81BD', '#C0504D', '#9BBB59', '#8064A2', '#1F497D', '#F79646', '#953735', '#4F6228', '#984807' 
    , '#4F81BD', '#C0504D', '#9BBB59', '#8064A2', '#1F497D', '#F79646', '#953735', '#4F6228', '#984807'
    , '#4F81BD', '#C0504D', '#9BBB59', '#8064A2', '#1F497D', '#F79646', '#953735', '#4F6228', '#984807' ]

nDiv = 1
timeLevels = [25,50,100,150,200]
dispFile = reader.ReadEFVLibInspectorFile("Terzaghi_6_Dt_0_1_EbFVM//GridYDisplacement_602.csv", nDiv, timeLevels)
presFile = reader.ReadEFVLibInspectorFile("Terzaghi_6_Dt_0_1_EbFVM//GridPressure_602.csv", nDiv, timeLevels)

currentTime = dispFile.getCurrentTime()
displacement = dispFile.getVariableData()
pressure = presFile.getVariableData()
yValues = presFile.getYAxisValues()
volumes = presFile.getVolumeValues()

## Calculando o comprimento característico da malha
h = 0
for i in range( len(volumes) ):
    h = h + volumes[i]
   
h = math.sqrt(h)/len( volumes )

anlCurrentTime = currentTime
anlDisplacement = []
anlPressure = []

## calculando a solução analitica

N = 200
o = analytical.TerzaghisProblemAnalytical( 6.0, 1.0e+6, 1.9e-15, 0.19, 0.001, 8.0e+9, 3.6e+10, 3.3e+9, 6.0e+9, 3.6e+10 )

for i in range( presFile.getNumberOfPlottingCurves() ):
    anlPressure.append( [] )
    anlDisplacement.append( [] )
    for j in range( len( volumes ) ):
        anlPressure[i].append( o.getPressureValue( yValues[j] , anlCurrentTime[i], N ) )
        anlDisplacement[i].append( o.getDisplacementValue( yValues[j] , anlCurrentTime[i], N ) )
    anlPressure[i] = np.array(anlPressure[i])
    anlDisplacement[i] = np.array(anlDisplacement[i])

## calculando o erro
presErro = []
dispErro = []

denErro = 0.0
numErro = 0.0
denErro1 = 0.0
numErro1 = 0.0
for i in range( presFile.getNumberOfPlottingCurves() ):
    for j in range( len( volumes ) ):
        numErro = numErro + ((pressure[i][j]- anlPressure[i][j])**2)*volumes[j] 
        denErro = denErro + (anlPressure[i][j]**2)*volumes[j] 
        numErro1 = numErro1 + ((displacement[i][j]- anlDisplacement[i][j])**2)*volumes[j] 
        denErro1 = denErro1 + (anlDisplacement[i][j]**2)*volumes[j] 
    presErro.append( math.sqrt( numErro/denErro ) )
    dispErro.append( math.sqrt( numErro1/denErro1 ) )
    denErro = 0.0
    numErro = 0.0
    denErro1 = 0.0
    numErro1 = 0.0
 
presErro = np.array(presErro)
dispErro = np.array(dispErro)   
   
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
plt.plot( anlCurrentTime, presErro, '-', color = color_list[1], linewidth = 0.95, label = 'Pressure error' )
plt.plot( anlCurrentTime, dispErro, '-', color = color_list[2], linewidth = 0.95, label = 'Vertical displacement error' )

## Mudando a posição e tamanho da área de plotagem
#box = axis.get_position()
#axis.set_position([box.x0-0.03, box.y0+0.03, box.width*0.7, box.height])

## linhas de grade posicionadas atrás das curvas plotadas
axis.set_axisbelow( True )
## Invertendo direção do Eixo X
#axis.invert_xaxis()

### Tamanho da fonte dos "labels" dos marcadores (ticks)
plt.tick_params( axis='both', which='major', labelsize=10) 
#
### Configurando a legenda e os "labels" dos eixos - - -  bbox_to_anchor = (1.05, 0.5)
plt.legend(loc = "upper right", numpoints = 1, fontsize = 12, frameon=True, title=r"\bf{Error x Time}" )
plt.ylabel( r" Error", size = 16)
plt.xlabel( r" Time(s) ", size = 16) 

####plt.savefig('C:\\Users\\ggrbill\\Desktop\\figure1.pdf')
#plt.show()