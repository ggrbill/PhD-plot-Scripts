# -*- coding: cp1252 -*-
"""
Created on Sun Jan 25 18:32:50 2015

@author: ggrbill
"""
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import TwoLayeredSoilAnalytical as analytical
import ReadEFVLibInspectorFile as reader
import MySort as s

color_list = [  '#4F81BD', '#C0504D', '#9BBB59', '#8064A2', '#1F497D', '#F79646', '#953735', '#4F6228', '#984807' 
    , '#4F81BD', '#C0504D', '#9BBB59', '#8064A2', '#1F497D', '#F79646', '#953735', '#4F6228', '#984807'
    , '#4F81BD', '#C0504D', '#9BBB59', '#8064A2', '#1F497D', '#F79646', '#953735', '#4F6228', '#984807' ]

#dispFile = open("Terzaghi_2Regions_0_Rk_10//ColumnYDisplacement_155.csv")
#presFile = open("Terzaghi_2Regions_0_Rk_10//ColumnPressure_155.csv")
#factor = 10.
#nDiv = 4

#dispFile = open("Terzaghi_2Regions_2_Rk_0_1//ColumnYDisplacement_155.csv")
#presFile = open("Terzaghi_2Regions_2_Rk_0_1//ColumnPressure_155.csv")
#factor = 0.1
#nDiv = 10
#dispFile = open("Terzaghi_2Regions_1_Rk_100_EBFVM//ColumnYDisplacement_602.csv")
#presFile = open("Terzaghi_2Regions_1_Rk_100_EBFVM//ColumnPressure_602.csv")
#factor = 100.
#nDiv = 4


factor = 100
factorName = "100"
infPerm = 1.9e-15
supPerm = factor * infPerm

nDiv = 4
numberOfCurves = 6
timeLevels = []
if factor == 0.1:
    timeLevels = [0,25,150,500,1000,2000]
if factor == 10:
    timeLevels = [0,25,100,250,500,1000]
if factor == 100:
    timeLevels = [0,25,100,250,500,1000]
        
dispFile = reader.ReadEFVLibInspectorFile("Terzaghi_2Regions_0_Rk_" + factorName + "_EBFVM//ColumnYDisplacement_91.csv", nDiv, timeLevels)
presFile = reader.ReadEFVLibInspectorFile("Terzaghi_2Regions_0_Rk_" + factorName + "_EBFVM//ColumnPressure_91.csv", nDiv, timeLevels)

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
#  height_1, permeability_1, phi_1, K_1, K_s_1, G_1, K_phi_1, 
#  height_2, permeability_2, phi_2, K_2, K_s_2, G_2, K_phi_2, mi, K_f, tao_0, p_0_1 = 0, p_0_2 = 0
 
# height, tao_0,  permeability, phi,  mi,    K,      K_s,     K_f,    G,      K_phi                     
# 6.0,    1.0e+6, 1.9e-15,      0.19, 0.001, 8.0e+9, 3.6e+10, 3.3e+9, 6.0e+9, 3.6e+10 
o = analytical.TwoLayeredSoilAnalytical( 3.0, supPerm, 0.19, 8.0e+9, 3.6e+10, 6.0e+9, 3.6e+10, 3.0, infPerm, 0.19, 8.0e+9, 3.6e+10, 6.0e+9, 3.6e+10, 0.001, 3.3e+9, 1.0e+6 )

anlYValues = o.getPositionValues()
anlYValues = np.array( anlYValues )

for i in range( presFile.getNumberOfPlottingCurves() ):
    anlPressure.append( np.array( o.getPressureValuesConstTime( anlCurrentTime[i], N ) ) )
    anlPressure[i] = anlPressure[i]/1000

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
    eYValues = yValues.copy()
    s.MySort( eYValues, displacement[i]  )
    plt.plot( displacement[i], eYValues, '-', linewidth = 0.9, color = color_list[i],   label = str( currentTime[i]) )

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

### Configurando a legenda e os "labels" dos eixos - - -  bbox_to_anchor = (1.05, 0.5)
plt.legend(loc = "center left", bbox_to_anchor = (1.05, 0.5), numpoints = 1, fontsize = 12, frameon=False, title=r"\bf{Tempos(s) }" )
#plt.legend(loc = "upper left", numpoints = 1, fontsize = 12, frameon=False, title=r"\bf{Time levels}" )
plt.ylabel( r" y(m)", size = 16)
plt.xlabel( r" Deslocamento vertical(mm) ", size = 16) 

###plt.savefig('C:\\Users\\ggrbill\\Desktop\\figure1.pdf')
plt.show()

## Criando o gráfico
fig = plt.figure( num = 2, figsize = (10,6) )
axis = plt.subplot(111)

plot_lines = []
## Plotando dados (função loglog) e linhas de grade (função grid)
plt.grid( True, which='both', axis='both', linestyle = '-', color = '#B5B5B5' )
for i in range(numberOfCurves):
    lines1, = plt.plot( anlPressure[i], anlYValues, '-', linewidth = 0.9, color = color_list[i], label = str( currentTime[i]) )
    lines2, = plt.plot( pressure[i], yValues, 'o', markeredgecolor = color_list[i], markersize = 4, color = color_list[i] )
    plot_lines.append( [lines1, lines2] )     


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

### Segunda legenda
second_legend = plt.legend(plot_lines[0], [ r"Anal\'{\i}tica", r"Num\'erica" ], loc=3, numpoints = 1, bbox_to_anchor = (1.04, 0.03) , fancybox=True, frameon=False, fontsize = 12, title = r"\bf{Solu\c{c}\~ao}" )
ax = plt.gca().add_artist(second_legend)

### Configurando a legenda e os "labels" dos eixos
plt.legend(loc = "center left", bbox_to_anchor = (1.04, 0.5), numpoints = 1, fontsize = 12, frameon=False, title=r"\bf{Tempos(s)}" )
###plt.legend(loc = "upper right", numpoints = 1, fontsize = 12, frameon=False, title=r"\bf{Pressure}" )
plt.ylabel( r" y(m)", size = 16)
plt.xlabel( r" Press\~ao(kPa) ", size = 16) 

###plt.savefig('C:\\Users\\ggrbill\\Desktop\\figure2.pdf')
plt.show()
