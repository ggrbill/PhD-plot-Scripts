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

## Lendo dados dos Arquivos
nDiv = 6
numberOfCurves = 4
#timeLevels = [0,25,200,500,1000,2000,3500]  #,400,600,1000,1500,2000,3500]
timeLevels = [0,100,1000,4000] 
numberOfCurves = len( timeLevels )


#uDispFile = reader.ReadEFVLibInspectorFile("Mandel_2_dt_0_1_FEM//uDisplacement_xdir_603.csv", nDiv, timeLevels)
#vDispFile = reader.ReadEFVLibInspectorFile("Mandel_2_dt_0_1_FEM//vDisplacement_ydir_603.csv", nDiv, timeLevels)
#presFile = reader.ReadEFVLibInspectorFile("Mandel_2_dt_0_1_FEM//Pressure_xdir_603.csv", nDiv, timeLevels)
#stressFile = reader.ReadEFVLibInspectorFile("Mandel_2_dt_0_1_FEM//Stress_xdir_603.csv", nDiv, timeLevels)

uDispFile = reader.ReadEFVLibInspectorFile("Mandel_Solution_57_Elements//uDisplacement_xdir_57.csv", nDiv, timeLevels)
vDispFile = reader.ReadEFVLibInspectorFile("Mandel_Solution_57_Elements//vDisplacement_ydir_57.csv", nDiv, timeLevels)
presFile = reader.ReadEFVLibInspectorFile("Mandel_Solution_57_Elements//Pressure_xdir_57.csv", nDiv, timeLevels)
stressFile = reader.ReadEFVLibInspectorFile("Mandel_Solution_57_Elements//Stress_xdir_57.csv", nDiv, timeLevels)


currentTime = uDispFile.getCurrentTime()
uDisplacement = uDispFile.getVariableData()
vDisplacement = vDispFile.getVariableData()
pressure = presFile.getVariableData()
stress = stressFile.getVariableData()

biot = 0.7777777777777777777777777777777777777777777
# Changing the Units (Pa->kPa, m->mm)  
# Computing Total Stress
for i in range ( uDispFile.getNumberOfPlottingCurves() ):
    uDisplacement[i] = uDisplacement[i]*1000000
    vDisplacement[i] = vDisplacement[i]*1000
    #pressure[i] = pressure[i]/1000
    stress[i] = biot*pressure[i] - stress[i]

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
    anluDisplacement.append( np.array( o.getHorDisplacementValuesConstTime( anlCurrentTime[i] ) )*1000000 )
    anlvDisplacement.append( np.array( o.getVertDisplacementValuesConstTime( anlCurrentTime[i] ) )*1000 )
    anlPressure.append( np.array( o.getPressureValuesConstTime( anlCurrentTime[i] ) ) )
    anlStress.append( -1.*np.array( o.getVertStressValuesConstTime( anlCurrentTime[i] ) ) )
       
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
        plt.plot( anlvDisplacement[i], anlyValues , '-', color = 'black', linewidth = 0.9, label = 'Analytical' )
        plt.plot( vDisplacement[i], yValues, 'o', color = 'black', markeredgecolor = 'black', markerfacecolor='none', markersize = 5, label = 'Numerical')
    else:
        plt.plot( anlvDisplacement[i], anlyValues , '-', color = 'black', linewidth = 0.9 )
        plt.plot( vDisplacement[i], yValues, 'o', color = 'black', markeredgecolor = 'black', markerfacecolor='none', markersize = 5 )
   

## Mudando a posição e tamanho da área de plotagem
#box = axis.get_position()
#axis.set_position([box.x0-0.03, box.y0+0.03, box.width*0.7, box.height])

##Colocando informação do tempo
axis.annotate("t = 0 s",
            xy=(-0.000095, 1.7), xycoords='data',
            xytext=(-0.000065, 1.8), textcoords='data',
            arrowprops=dict(arrowstyle="->",
                            connectionstyle="arc3"),
            )

axis.annotate("t = 100 s",
            xy=(-0.000089, 1.55), xycoords='data',
            xytext=(-0.000055, 1.65), textcoords='data',
            arrowprops=dict(arrowstyle="->",
                            connectionstyle="arc3"),
            )
            
axis.annotate("t = 1000 s",
            xy=(-0.00010, 1.675), xycoords='data',
            xytext=(-0.000115, 1.52), textcoords='data',
            arrowprops=dict(arrowstyle="->",
                            connectionstyle="arc3"),
            )

axis.annotate("t = 4000 s",
            xy=(-0.000095, 1.475), xycoords='data',
            xytext=(-0.000105, 1.35), textcoords='data',
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
#plt.legend(loc = "center left", bbox_to_anchor = (1.05, 0.5), numpoints = 1, fontsize = 12, frameon=False, title=r"\bf{Time(s)}" )
plt.legend(loc = "lower right", numpoints = 1, fontsize = 12, frameon=True )
plt.ylabel( r" y(m)", size = 16)
plt.xlabel( r" Vertical displacement(mm) ", size = 16) 

plt.savefig('C:\\Users\\ggrbill\\Desktop\\figure1.pdf')
plt.show()



## Criando o gráfico
fig = plt.figure( num = 2, figsize = (7,6) )
axis = plt.subplot(111)

## Plotando dados (função loglog) e linhas de grade (função grid)
plt.grid( True, which='both', axis='both', linestyle = '-', color = '#B5B5B5' )
for i in range(numberOfCurves):
    if i == numberOfCurves-1:
        plt.plot(  anlxValues, anluDisplacement[i], '-', color = 'black', linewidth = 0.9, label = 'Analytical' )
        plt.plot(  xValues, uDisplacement[i], 'o', color = 'black', markeredgecolor = 'black', markerfacecolor='none', markersize = 5, label = 'Numerical')
    else:
        plt.plot( anlxValues, anluDisplacement[i], '-', color = 'black', linewidth = 0.9 )
        plt.plot( xValues, uDisplacement[i], 'o', color = 'black', markeredgecolor = 'black', markerfacecolor='none', markersize = 5 )
   
## Mudando a posição e tamanho da área de plotagem
#box = axis.get_position()
#axis.set_position([box.x0-0.03, box.y0+0.03, box.width*0.7, box.height])
   
##Colocando informação do tempo
axis.annotate("t = 0 s",
            xy=(9.5, 0.265), xycoords='data',
            xytext=(7.5, 0.28), textcoords='data',
            arrowprops=dict(arrowstyle="->",
                            connectionstyle="arc3"),
            )

axis.annotate("t = 100 s",
            xy=(6.25, 0.18), xycoords='data',
            xytext=(4.3, 0.21), textcoords='data',
            arrowprops=dict(arrowstyle="->",
                            connectionstyle="arc3"),
            )
            
axis.annotate("t = 1000 s",
            xy=(5.65, 0.145), xycoords='data',
            xytext=(6.25, 0.09), textcoords='data',
            arrowprops=dict(arrowstyle="->",
                            connectionstyle="arc3"),
            )

axis.annotate("t = 4000 s",
            xy=(7.2, 0.14), xycoords='data',
            xytext=(8.15, 0.105), textcoords='data',
            arrowprops=dict(arrowstyle="->",
                            connectionstyle="arc3"),
            )      

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

### Configurando a legenda e os "labels" dos eixos - - -  bbox_to_anchor = (1.05, 0.5)
#plt.legend(loc = "center left", bbox_to_anchor = (1.05, 0.5), numpoints = 1, fontsize = 12, frameon=False, title=r"\bf{Time(s)}" )
plt.legend(loc = "lower right", numpoints = 1, fontsize = 12, frameon=True )
plt.ylabel( r" Horizontal displacement($\mu$m)", size = 16)
plt.xlabel( r" x(m) ", size = 16) 

plt.savefig('C:\\Users\\ggrbill\\Desktop\\figure2.pdf')
plt.show()


## Criando o gráfico
fig = plt.figure( num = 3, figsize = (7,6) )
axis = plt.subplot(111)

## Plotando dados (função loglog) e linhas de grade (função grid)
plt.grid( True, which='both', axis='both', linestyle = '-', color = '#B5B5B5' )
for i in range(numberOfCurves):
    if i == numberOfCurves-1:
        plt.plot( anlxValues, anlPressure[i] , '-', linewidth = 0.9, color = 'black', label = 'Analytical' )
        plt.plot( xValues, pressure[i], 'o', color = 'black', markeredgecolor = 'black', markerfacecolor='none', markersize = 5, label = ' Numerical')
    else:
        plt.plot( anlxValues, anlPressure[i] , '-', linewidth = 0.9, color = 'black' )
        plt.plot(  xValues, pressure[i], 'o', color = 'black', markeredgecolor = 'black', markerfacecolor='none', markersize = 5 )

## Mudando a posição e tamanho da área de plotagem
#box = axis.get_position()
#axis.set_position([box.x0-0.03, box.y0+0.03, box.width*0.7, box.height])

##Colocando informação do tempo
axis.annotate("t = 0 s",
            xy=(8.8, 287.5), xycoords='data',
            xytext=(8.5, 255), textcoords='data',
            arrowprops=dict(arrowstyle="->",
                            connectionstyle="arc3"),
            )

axis.annotate("t = 100 s",
            xy=(7, 265), xycoords='data',
            xytext=(5.5, 225), textcoords='data',
            arrowprops=dict(arrowstyle="->",
                            connectionstyle="arc3"),
            )
            
axis.annotate("t = 1000 s",
            xy=(3.6, 223), xycoords='data',
            xytext=(2.2, 185), textcoords='data',
            arrowprops=dict(arrowstyle="->",
                            connectionstyle="arc3"),
            )

axis.annotate("t = 4000 s",
            xy=(2.1, 87), xycoords='data',
            xytext=(2.2, 112), textcoords='data',
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

## Configurando a legenda e os "labels" dos eixos
#plt.legend(loc = "center left", bbox_to_anchor = (1.05, 0.5), numpoints = 1, fontsize = 12, frameon=False, title=r"\bf{Time(s)}" )
plt.legend(loc = "lower left", numpoints = 1, fontsize = 12, frameon=True )
plt.ylabel( r" Pressure(Pa)", size = 16)
plt.xlabel( r" x(m) ", size = 16) 

plt.savefig('C:\\Users\\ggrbill\\Desktop\\figure3.pdf')
plt.show()

## Criando o gráfico
fig = plt.figure( num = 4, figsize = (7,6) )
axis = plt.subplot(111)

## Plotando dados (função loglog) e linhas de grade (função grid)
plt.grid( True, which='both', axis='both', linestyle = '-', color = '#B5B5B5' )
for i in range(numberOfCurves):
    if i == numberOfCurves-1:
        plt.plot( anlxValues, anlStress[i] , '-', linewidth = 1.0, color = 'black', label = 'Analytical' )
        plt.plot( xValues, stress[i], 'o', color = 'black', markeredgecolor = 'black', markerfacecolor='none', markersize = 5, label = ' Numerical')
    else:
        plt.plot( anlxValues, anlStress[i] , '-', linewidth = 0.9, color = 'black' )
        plt.plot(  xValues, stress[i], 'o', color = 'black', markeredgecolor = 'black', markerfacecolor='none', markersize = 5 )
    
## Mudando a posição e tamanho da área de plotagem
#box = axis.get_position()
#axis.set_position([box.x0-0.03, box.y0+0.03, box.width*0.7, box.height])

##Colocando informação do tempo
axis.annotate("t = 0 s",
            xy=(8.9, 1002), xycoords='data',
            xytext=(8.5, 1035), textcoords='data',
            arrowprops=dict(arrowstyle="->",
                            connectionstyle="arc3"),
            )

axis.annotate("t = 100 s",
            xy=(6.5, 1020), xycoords='data',
            xytext=(6.5, 1055), textcoords='data',
            arrowprops=dict(arrowstyle="->",
                            connectionstyle="arc3"),
            )
            
axis.annotate("t = 1000 s",
            xy=(2.7, 1044), xycoords='data',
            xytext=(2.3, 1075), textcoords='data',
            arrowprops=dict(arrowstyle="->",
                            connectionstyle="arc3"),
            )

axis.annotate("t = 4000 s",
            xy=(2.1, 1016), xycoords='data',
            xytext=(1.6, 965), textcoords='data',
            arrowprops=dict(arrowstyle="->",
                            connectionstyle="arc3"),
            )     

## linhas de grade posicionadas atrás das curvas plotadas
axis.set_axisbelow( True )

#### Tamanho da fonte dos "labels" dos marcadores (ticks)
plt.tick_params( axis='both', which='major', labelsize=12)

## Configurando a legenda e os "labels" dos eixos
#plt.legend(loc = "center left", bbox_to_anchor = (1.05, 0.5), numpoints = 1, fontsize = 12, frameon=False, title=r"\bf{Time(s)}" )
plt.legend(loc = "lower left", numpoints = 1, fontsize = 12, frameon=True )
plt.ylabel( r" Vertical Stress(Pa)", size = 16)
plt.xlabel( r" x(m) ", size = 16) 

plt.savefig('C:\\Users\\ggrbill\\Desktop\\figure4.pdf')
plt.show()
