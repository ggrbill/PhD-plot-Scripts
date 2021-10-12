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
numberOfCurves = 4
timeLevels = [50,500,1000,2000]
dispFile = reader.ReadEFVLibInspectorFile("Terzaghi_Solution_91_Elements//ColumnYDisplacement_91.csv", nDiv, timeLevels)
presFile = reader.ReadEFVLibInspectorFile("Terzaghi_Solution_91_Elements//ColumnPressure_91.csv", nDiv, timeLevels)

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
#                                         height, F, permeability, phi, mi,     K,      K_s,    K_f,     G,     K_phi 
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
fig = plt.figure( num = 1, figsize = (7,6) )
axis = plt.subplot(111)

## Plotando dados (função loglog) e linhas de grade (função grid)
plt.grid( True, which='both', axis='both', linestyle = '-', color = '#B5B5B5' )
for i in range(numberOfCurves):
    if i == numberOfCurves-1:
        plt.plot( anlDisplacement[i], anlYValues , '-', color = 'black', linewidth = 0.9, label = 'Analytical' )
        plt.plot( displacement[i], yValues, 'o', markerfacecolor='none', markeredgecolor = 'black', markersize = 4, color = 'black', label = 'Numerical')
    else:
        plt.plot( anlDisplacement[i], anlYValues , '-', color = 'black', linewidth = 0.9 )
        plt.plot( displacement[i], yValues, 'o', markerfacecolor='none', markeredgecolor = 'black', markersize = 4, color = 'black')

## Mudando a posição e tamanho da área de plotagem
#box = axis.get_position()
#axis.set_position([box.x0-0.03, box.y0+0.03, box.width*0.7, box.height])

##Colocando informação do tempo
axis.annotate("t = 50 s",
            xy=(-0.205, 4.85), xycoords='data',
            xytext=(-0.14, 5.5), textcoords='data',
            arrowprops=dict(arrowstyle="->",
                            connectionstyle="arc3"),
            )

axis.annotate("t = 500 s",
            xy=(-0.19, 3.8), xycoords='data',
            xytext=(-0.09, 4.5), textcoords='data',
            arrowprops=dict(arrowstyle="->",
                            connectionstyle="arc3"),
            )
            
axis.annotate("t = 1000 s",
            xy=(-0.198, 3.58), xycoords='data',
            xytext=(-0.23, 2.5), textcoords='data',
            arrowprops=dict(arrowstyle="->",
                            connectionstyle="arc3"),
            )

axis.annotate("t = 2000 s",
            xy=(-0.26, 4.3), xycoords='data',
            xytext=(-0.29, 3.5), textcoords='data',
            arrowprops=dict(arrowstyle="->",
                            connectionstyle="arc3"),
            )      

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

### Configurando a legenda e os "labels" dos eixos - - -  bbox_to_anchor = (1.05, 0.5)
plt.legend(loc = "lower right", numpoints = 1, fontsize = 12, frameon=True )
#plt.legend(loc = "center left", bbox_to_anchor = (1.05, 0.5), numpoints = 1, fontsize = 12, frameon=False, title=r"\bf{Time(s)}" )
plt.ylabel( r" y(m)", size = 16)
plt.xlabel( r" Vertical displacement(mm) ", size = 16) 

#plt.savefig('C:\\Users\\ggrbill\\Desktop\\figure1.pdf')
plt.show()

## Criando o gráfico
fig = plt.figure( num = 2, figsize = (7,6) )
axis = plt.subplot(111)

## Plotando dados (função loglog) e linhas de grade (função grid)
plt.grid( True, which='both', axis='both', linestyle = '-', color = '#B5B5B5' )
for i in range(numberOfCurves):
    if i == numberOfCurves-1:
        plt.plot( anlPressure[i], anlYValues, '-', linewidth = 0.9, color = 'black', label = 'Analytical' )
        plt.plot( pressure[i], yValues, 'o', markerfacecolor='none', markeredgecolor = 'black', markersize = 4, color = 'black', label = ' Numerical' )
    else:
        plt.plot( anlPressure[i], anlYValues, '-', linewidth = 0.9, color = 'black' )
        plt.plot( pressure[i], yValues, 'o', markerfacecolor='none', markeredgecolor = 'black', markersize = 4, color = 'black')

## Mudando a posição e tamanho da área de plotagem
#box = axis.get_position()
#axis.set_position([box.x0-0.03, box.y0+0.03, box.width*0.7, box.height])

##Colocando informação do tempo
axis.annotate("t = 50 s",
            xy=(285, 4.75), xycoords='data',
            xytext=(230, 4.1), textcoords='data',
            arrowprops=dict(arrowstyle="->",
                            connectionstyle="arc3"),
            )

axis.annotate("t = 500 s",
            xy=(213, 3.1), xycoords='data',
            xytext=(260, 3.4), textcoords='data',
            arrowprops=dict(arrowstyle="->",
                            connectionstyle="arc3"),
            )
            
axis.annotate("t = 1000 s",
            xy=(159, 1.6), xycoords='data',
            xytext=(180, 2.05), textcoords='data',
            arrowprops=dict(arrowstyle="->",
                            connectionstyle="arc3"),
            )

axis.annotate("t = 2000 s",
            xy=(52, 1.3), xycoords='data',
            xytext=(85, 0.8), textcoords='data',
            arrowprops=dict(arrowstyle="->",
                            connectionstyle="arc3"),
            )      

## linhas de grade posicionadas atrás das curvas plotadas
axis.set_axisbelow( True )

#### Tamanho da fonte dos "labels" dos marcadores (ticks)
plt.tick_params( axis='both', which='major', labelsize=12) 

### Limites dos eixos
xMin, xMax = plt.xlim()
plt.xlim( 0.0, xMax )
yMin, yMax = plt.ylim()
plt.ylim( 0.0, yMax )

### Configurando a legenda e os "labels" dos eixos
##plt.legend(loc = "center left", bbox_to_anchor = (1.05, 0.5), numpoints = 1, fontsize = 12, frameon=False, title=r"\bf{Time(s)}" )
plt.legend(loc = "upper right", numpoints = 1, fontsize = 12, frameon=True )
plt.ylabel( r" y(m)", size = 16)
plt.xlabel( r" Pressure(kPa) ", size = 16) 

#plt.savefig('C:\\Users\\ggrbill\\Desktop\\figure2.pdf')
#plt.savefig('C:\\Users\\ggrbill\\Desktop\\figure2.tiff' , format='tiff', dpi=600)
plt.show()
