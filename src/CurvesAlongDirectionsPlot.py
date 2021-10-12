# -*- coding: cp1252 -*-
"""
Created on Sun Jan 25 18:32:50 2015

@author: ggrbill
"""
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import MandelsProblemAnalytical as analytical
import ReadEFVLibInspectorFile as reader

color_list = [  '#4F81BD', '#C0504D', '#9BBB59', '#8064A2', '#1F497D', '#F79646', '#953735', '#4F6228', '#984807' 
    , '#4F81BD', '#C0504D', '#9BBB59', '#8064A2', '#1F497D', '#F79646', '#953735', '#4F6228', '#984807'
    , '#4F81BD', '#C0504D', '#9BBB59', '#8064A2', '#1F497D', '#F79646', '#953735', '#4F6228', '#984807' ]

plt.close('all')

## Lendo dados dos Arquivos
nDiv = 6
numberOfCurves = 4
timeLevels = [0,30,200,500,1000,2000,3500]  #,400,600,1000,1500,2000,3500]
#timeLevels = [0,20,50,70,100] 
numberOfCurves = len( timeLevels )

grid = "228"
#uDispFile = reader.ReadEFVLibInspectorFile("Mandel_2_dt_0_1_FEM//uDisplacement_xdir_603.csv", nDiv, timeLevels)
#vDispFile = reader.ReadEFVLibInspectorFile("Mandel_2_dt_0_1_FEM//vDisplacement_ydir_603.csv", nDiv, timeLevels)
#presFile = reader.ReadEFVLibInspectorFile("Mandel_2_dt_0_1_FEM//Pressure_xdir_603.csv", nDiv, timeLevels)
#stressFile = reader.ReadEFVLibInspectorFile("Mandel_2_dt_0_1_FEM//Stress_xdir_603.csv", nDiv, timeLevels)
dt = "1"
method = "EbFVM"

uDispFile = reader.ReadEFVLibInspectorFile("Mandel_2_Convergence//Mandel_2_Dt_" + dt + "_" + method + "//uDisplacement_xdir_" + grid + ".csv", nDiv, timeLevels)
vDispFile = reader.ReadEFVLibInspectorFile("Mandel_2_Convergence//Mandel_2_Dt_" + dt + "_" + method + "//vDisplacement_ydir_" + grid + ".csv", nDiv, timeLevels)
presFile = reader.ReadEFVLibInspectorFile("Mandel_2_Convergence//Mandel_2_Dt_" + dt + "_" + method + "//Pressure_xdir_" + grid + ".csv", nDiv, timeLevels)
stressFile = reader.ReadEFVLibInspectorFile("Mandel_2_Convergence//Mandel_2_Dt_" + dt + "_" + method + "//Stress_xdir_" + grid + ".csv", nDiv, timeLevels)


currentTime = uDispFile.getCurrentTime()
uDisplacement = uDispFile.getVariableData()
vDisplacement = vDispFile.getVariableData()
pressure = presFile.getVariableData()
stress = stressFile.getVariableData()

#biot = 0.7777777777777777777777777777777777777777777
biot = 0.777777777778
# Changing the Units (Pa->kPa, m->mm)  
# Computing Total Stress
for i in range ( uDispFile.getNumberOfPlottingCurves() ):
    uDisplacement[i] = uDisplacement[i]*1000
    vDisplacement[i] = vDisplacement[i]*1000
    pressure[i] = pressure[i]/1000
    stress[i] = biot*pressure[i] - stress[i]/1000

anlCurrentTime = currentTime
anlvDisplacement = []
anluDisplacement = []
anlPressure = []
anlStress = []

yValues = vDispFile.getYAxisValues()
xValues = uDispFile.getXAxisValues()
anlYValues = []
anlxValues = []

## calculando a solução analitica
N = 1000
# lenght, height, F, permeability, phi, mi, K, K_s, K_f, G, K_phi 
o = analytical.MandelsProblemAnalytical( 10.0, 2.0, 1.0e+4, 1.9e-15, 0.19, 0.001, 8.0e+9, 3.6e+10, 3.3e+9, 6.0e+9, 3.6e+10 )
#o = analytical.MandelsProblemAnalytical( 5.0, 5.0, 5.0e+7, 1.e-15, 0.19, 0.001, 8.0e+9, 3.6e+10, 3.3e+9, 6.0e+9, 3.6e+10 )

anlxValues = np.array( o.getXPositionValues() )
anlyValues = np.array( o.getYPositionValues() )

for i in range( uDispFile.getNumberOfPlottingCurves() ):
    anluDisplacement.append( np.array( o.getHorDisplacementValuesConstTime( anlCurrentTime[i] ) )*1000 )
    anlvDisplacement.append( np.array( o.getVertDisplacementValuesConstTime( anlCurrentTime[i] ) )*1000 )
    anlPressure.append( np.array( o.getPressureValuesConstTime( anlCurrentTime[i] ) ) / 1000 )
    anlStress.append( -1.*np.array( o.getVertStressValuesConstTime( anlCurrentTime[i] ) ) /1000 )
       
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
    lines1, = plt.plot( anlvDisplacement[i], anlyValues , '-', color = color_list[i], linewidth = 0.9, label = str( currentTime[i]) )
    lines2, = plt.plot( vDisplacement[i], yValues, 'o', markeredgecolor = color_list[i], markersize = 4, color = color_list[i])
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

### Segunda Legenda
first_legend = plt.legend(plot_lines1[0], [ r"Anal\'{\i}tica", r"Num\'erica" ], loc=3, numpoints = 1, bbox_to_anchor = (1.04, 0.03) , fancybox=True, frameon=False, fontsize = 12, title = r"\bf{Solu\c{c}\~ao}" )
ax = plt.gca().add_artist(first_legend)

### Configurando a legenda e os "labels" dos eixos - - -  bbox_to_anchor = (1.05, 0.5)
plt.legend(loc = "center left", bbox_to_anchor = (1.04, 0.5), numpoints = 1, fontsize = 12, frameon=False, title=r"\bf{Tempos(s)}" )
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
    lines1, = plt.plot(  anlxValues, anluDisplacement[i], '-', color = color_list[i], linewidth = 0.9, label = str( currentTime[i]) )
    lines2, = plt.plot(  xValues, uDisplacement[i], 'o', markeredgecolor = color_list[i], markersize = 4, color = color_list[i])
    plot_lines2.append( [lines1, lines2] )
   
## Mudando a posição e tamanho da área de plotagem
box = axis.get_position()
axis.set_position([box.x0-0.03, box.y0+0.03, box.width*0.7, box.height])

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
plt.ylim( 0.0, yMax )

### Segunda Legenda
first_legend = plt.legend(plot_lines2[0], [ r"Anal\'{\i}tica", r"Num\'erica" ], loc=3, numpoints = 1, bbox_to_anchor = (1.04, 0.03) , fancybox=True, frameon=False, fontsize = 12, title = r"\bf{Solu\c{c}\~ao}" )
ax = plt.gca().add_artist(first_legend)

### Configurando a legenda e os "labels" dos eixos - - -  bbox_to_anchor = (1.05, 0.5)
plt.legend(loc = "center left", bbox_to_anchor = (1.04, 0.5), numpoints = 1, fontsize = 12, frameon=False, title=r"\bf{Tempos(s)}" )
#plt.legend(loc = "upper left", numpoints = 1, fontsize = 12, frameon=False, title=r"\bf{Time levels}" )
plt.ylabel( r" Deslocamento horizontal(mm)", size = 16)
plt.xlabel( r" x(m) ", size = 16) 

###plt.savefig('C:\\Users\\ggrbill\\Desktop\\figure1.pdf')
plt.show()



## Criando o gráfico
fig = plt.figure( num = 3, figsize = (10,6) )
axis = plt.subplot(111)

plot_lines3 = []
## Plotando dados (função loglog) e linhas de grade (função grid)
plt.grid( True, which='both', axis='both', linestyle = '-', color = '#B5B5B5' )
for i in range(numberOfCurves):
    lines1, = plt.plot( anlxValues, anlPressure[i] , '-', linewidth = 0.9, color = color_list[i], label = str( currentTime[i]))
    lines2, = plt.plot( xValues, pressure[i], 'o', markeredgecolor = color_list[i], markersize = 4, color = color_list[i] )
    plot_lines3.append( [lines1, lines2] )

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

### Segunda Legenda
first_legend = plt.legend(plot_lines3[0], [ r"Anal\'{\i}tica", r"Num\'erica" ], loc=3, numpoints = 1, bbox_to_anchor = (1.04, 0.03) , fancybox=True, frameon=False, fontsize = 12, title = r"\bf{Solu\c{c}\~ao}" )
ax = plt.gca().add_artist(first_legend)

## Configurando a legenda e os "labels" dos eixos
plt.legend(loc = "center left", bbox_to_anchor = (1.04, 0.5), numpoints = 1, fontsize = 12, frameon=False, title=r"\bf{Tempos(s)}" )
###plt.legend(loc = "upper right", numpoints = 1, fontsize = 12, frameon=False, title=r"\bf{Pressure}" )
plt.ylabel( r" Press\~ao(kPa) ", size = 16)
plt.xlabel( r" x(m) ", size = 16) 

###plt.savefig('C:\\Users\\ggrbill\\Desktop\\figure2.pdf')
plt.show()

## Criando o gráfico
fig = plt.figure( num = 4, figsize = (10,6) )
axis = plt.subplot(111)

plot_lines4 = []
## Plotando dados (função loglog) e linhas de grade (função grid)
plt.grid( True, which='both', axis='both', linestyle = '-', color = '#B5B5B5' )
for i in range(numberOfCurves):
    lines1, = plt.plot( anlxValues, anlStress[i] , '-', linewidth = 0.9, color = color_list[i], label = str( currentTime[i]))
    lines2, = plt.plot( xValues, stress[i], 'o', markeredgecolor = color_list[i], markersize = 4, color = color_list[i])
    plot_lines4.append( [lines1, lines2] )
    
## Mudando a posição e tamanho da área de plotagem
box = axis.get_position()
axis.set_position([box.x0-0.03, box.y0+0.03, box.width*0.7, box.height])

## linhas de grade posicionadas atrás das curvas plotadas
axis.set_axisbelow( True )

#### Tamanho da fonte dos "labels" dos marcadores (ticks)
plt.tick_params( axis='both', which='major', labelsize=12)

### Segunda Legenda
first_legend = plt.legend(plot_lines4[0], [ r"Anal\'{\i}tica", r"Num\'erica" ], loc=3, numpoints = 1, bbox_to_anchor = (1.04, 0.03) , fancybox=True, frameon=False, fontsize = 12, title = r"\bf{Solu\c{c}\~ao}" )
ax = plt.gca().add_artist(first_legend)

## Configurando a legenda e os "labels" dos eixos
plt.legend(loc = "center left", bbox_to_anchor = (1.04, 0.5), numpoints = 1, fontsize = 12, frameon=False, title=r"\bf{Tempos(s)}" )
###plt.legend(loc = "upper right", numpoints = 1, fontsize = 12, frameon=False, title=r"\bf{Pressure}" )
plt.ylabel( r" Tens\~ao total vertical(kPa)", size = 16)
plt.xlabel( r" x(m) ", size = 16) 

###plt.savefig('C:\\Users\\ggrbill\\Desktop\\figure2.pdf')
plt.show()
