# -*- coding: cp1252 -*-
"""
Created on Sun Jan 25 18:32:50 2015

@author: ggrbill
"""
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import TerzaghisProblemAnalytical as analytical
import ReadEFVLibInspectorFile as reader

color_list = [  '#4F81BD', '#C0504D', '#9BBB59', '#8064A2', '#1F497D', '#F79646', '#953735', '#4F6228', '#984807' 
    , '#4F81BD', '#C0504D', '#9BBB59', '#8064A2', '#1F497D', '#F79646', '#953735', '#4F6228', '#984807'
    , '#4F81BD', '#C0504D', '#9BBB59', '#8064A2', '#1F497D', '#F79646', '#953735', '#4F6228', '#984807' ]

## Lendo dados dos Arquivos
nDiv = 1
numberOfCurves = 7
timeLevels = [0,10,100,300,600,1200,4000]
dispFile = reader.ReadEFVLibInspectorFile("Time_Solution_Grid_H1_91_elem//ColumnYDisplacement_91.csv", nDiv, timeLevels)
presFile = reader.ReadEFVLibInspectorFile("Time_Solution_Grid_H1_91_elem//ColumnPressure_91.csv", nDiv, timeLevels)

currentTime = dispFile.getCurrentTime()
displacement = dispFile.getVariableData()
pressure = presFile.getVariableData()
yValues = presFile.getYAxisValues()

# Changing the Units (Pa->kPa, m->mm)  
for i in range ( presFile.getNumberOfPlottingCurves() ):
    displacement[i] = displacement[i]*1000
    pressure[i] = pressure[i]/1000

anlCurrentTime = currentTime
anlDisplacement = []
anlPressure = []
anlYValues = []

## calculando a solução analitica
N = 200
o = analytical.TerzaghisProblemAnalytical( 6.0, 1.0e+6, 1.9e-15, 0.19, 0.001, 8.0e+9, 3.6e+10, 3.3e+9, 6.0e+9, 3.6e+10 )

anlYValues = o.getPositionValues()
anlYValues = np.array( anlYValues )

for i in range( presFile.getNumberOfPlottingCurves() ):
    anlDisplacement.append( o.getDisplacementValuesConstTime( anlCurrentTime[i] ) )
    anlPressure.append(o.getPressureValuesConstTime( anlCurrentTime[i] )  )
    anlDisplacement[i] = np.array(anlDisplacement[i])
    anlPressure[i] = np.array(anlPressure[i])
    anlDisplacement[i] = anlDisplacement[i]*1000
    anlPressure[i] = anlPressure[i]/1000


######## PLOTANDO OS GRÁFICOS ############

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

plot_lines1 = []
## Plotando dados (função loglog) e linhas de grade (função grid)
plt.grid( True, which='both', axis='both', linestyle = '-', color = '#B5B5B5' )
for i in range(numberOfCurves):
    lines1, = plt.plot( anlDisplacement[i], anlYValues , '-', color = color_list[i], linewidth = 0.9, label = str( currentTime[i]) )
    lines2, = plt.plot( displacement[i], yValues, 'o', markeredgecolor = color_list[i], markersize = 4, color = color_list[i] )
    plot_lines1.append( [lines1, lines2] )

## Mudando a posição e tamanho da área de plotagem
box = axis.get_position()
axis.set_position([box.x0-0.03, box.y0+0.03, box.width*0.7, box.height])

## linhas de grade posicionadas atrás das curvas plotadas
axis.set_axisbelow( True )
## Invertendo direção do Eixo X
axis.invert_xaxis()
#
### Tamanho da fonte dos "labels" dos marcadores (ticks)
plt.tick_params( axis='both', which='major', labelsize=12) 

### Limites dos eixos
xMin, xMax = plt.xlim()
plt.xlim( 0.0, xMax )
yMin, yMax = plt.ylim()
plt.ylim( 0.0, yMax )

### Tem mais coisa lá embaixo
first_legend = plt.legend(plot_lines1[0], [ r"Anal\'{\i}tica", r"Num\'erica" ], loc=3, numpoints = 1, bbox_to_anchor = (1.04, 0.03) , fancybox=True, frameon=False, fontsize = 12, title = r"\bf{Solu\c{c}\~ao}" )
ax = plt.gca().add_artist(first_legend)

### Configurando a legenda e os "labels" dos eixos - - -  bbox_to_anchor = (1.05, 0.5)
plt.legend(loc = "center left", bbox_to_anchor = (1.04, 0.5), numpoints = 1, fontsize = 12, fancybox=True, frameon=False, title=r"\bf{Tempos(s)}" )
#plt.legend(loc = "upper left", numpoints = 1, fontsize = 12, frameon=False, title=r"\bf{Time levels}" )
plt.ylabel( r" y(m)", size = 16)
plt.xlabel( r" Deslocamento vertical(mm) ", size = 16) 

###plt.savefig('C:\\Users\\ggrbill\\Desktop\\figure1.pdf')
plt.show()



## Criando o gráfico
fig = plt.figure( num = 2, figsize = (10,6) )
axis = plt.subplot(111)

plot_lines2 = []
## Plotando dados (função loglog) e linhas de grade (função grid)
plt.grid( True, which='both', axis='both', linestyle = '-', color = '#B5B5B5' )
for i in range(numberOfCurves):
   lines1, = plt.plot( anlPressure[i], anlYValues, '-', linewidth = 0.9, color = color_list[i], label = str( currentTime[i]))
   lines2, = plt.plot( pressure[i], yValues, 'o', markeredgecolor = color_list[i], markersize = 4, color = color_list[i])
   plot_lines2.append( [lines1, lines2] )

## Mudando a posição e tamanho da área de plotagem
box = axis.get_position()
axis.set_position([box.x0-0.03, box.y0+0.03, box.width*0.7, box.height])

## linhas de grade posicionadas atrás das curvas plotadas
axis.set_axisbelow( True )

#### Tamanho da fonte dos "labels" dos marcadores (ticks)
plt.tick_params( axis='both', which='major', labelsize=12) 

### Limites dos eixos
xMin, xMax = plt.xlim()
plt.xlim( 0.0, xMax )
yMin, yMax = plt.ylim()
plt.ylim( 0.0, yMax )

###
#plot_lines = []
#dado1 = [-1]
#dado1 = np.array( dado1 )
#lines1, = plt.plot( dado1, '-', color = 'black' , label = r"Anal\'{\i}tica" )
#lines2, = plt.plot( dado1, 'o', color = 'black' , label = r"Num\'erica" )    
#plot_lines.append( [lines1, lines2] )
second_legend = plt.legend(plot_lines2[0], [ r"Anal\'{\i}tica", r"Num\'erica" ], loc=3, numpoints = 1, bbox_to_anchor = (1.04, 0.03) , fancybox=True, frameon=False, fontsize = 12, title = r"\bf{Solu\c{c}\~ao}" )
ax = plt.gca().add_artist(second_legend)

### Configurando a legenda e os "labels" dos eixos
plt.legend( loc = "center left", bbox_to_anchor = (1.04, 0.5), numpoints = 1, fontsize = 12, fancybox=True, frameon=False, title=r"\bf{Tempos(s)}" )
###plt.legend(loc = "upper right", numpoints = 1, fontsize = 12, frameon=False, title=r"\bf{Pressure}" )
plt.ylabel( r" y(m)", size = 16)
plt.xlabel( r" Press\~ao(kPa) ", size = 16) 



###plt.savefig('C:\\Users\\ggrbill\\Desktop\\figure2.pdf')
plt.show()
