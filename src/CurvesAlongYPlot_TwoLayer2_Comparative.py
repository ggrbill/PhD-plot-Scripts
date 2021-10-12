# -*- coding: cp1252 -*-
"""
Created on Sun Jan 25 18:32:50 2015

@author: ggrbill
"""
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import ReadEFVLibInspectorFile as reader
import MySort as s

color_list = [  '#4F81BD', '#C0504D', '#9BBB59', '#8064A2', '#1F497D', '#F79646', '#953735', '#4F6228', '#984807' 
    , '#4F81BD', '#C0504D', '#9BBB59', '#8064A2', '#1F497D', '#F79646', '#953735', '#4F6228', '#984807'
    , '#4F81BD', '#C0504D', '#9BBB59', '#8064A2', '#1F497D', '#F79646', '#953735', '#4F6228', '#984807' ]

#dispFile = open("Terzaghi_2Regions_3_Dif_Mec_fem//ColumnYDisplacement_155.csv")
#presFile = open("Terzaghi_2Regions_3_Dif_Mec_fem//ColumnPressure_155.csv")
#nDiv = 8


nDiv = 4
numberOfCurves = 8
timeLevels = [0,500,1000,1500,2000]
numberOfCurves = len( timeLevels )
EBFVMdispFile = reader.ReadEFVLibInspectorFile("Terzaghi_2Regions_3_Dif_Mec_EBFVM//ColumnYDisplacement_602.csv", nDiv, timeLevels)
EBFVMpresFile = reader.ReadEFVLibInspectorFile("Terzaghi_2Regions_3_Dif_Mec_EBFVM//ColumnPressure_602.csv", nDiv, timeLevels)
FEMdispFile = reader.ReadEFVLibInspectorFile("Terzaghi_2Regions_3_Dif_Mec_FEM//ColumnYDisplacement_602.csv", nDiv, timeLevels)
FEMpresFile = reader.ReadEFVLibInspectorFile("Terzaghi_2Regions_3_Dif_Mec_FEM//ColumnPressure_602.csv", nDiv, timeLevels)

currentTime = EBFVMdispFile.getCurrentTime()
EBFVMdisplacement = EBFVMdispFile.getVariableData()
EBFVMpressure = EBFVMpresFile.getVariableData()
EBFVMyValues = EBFVMpresFile.getYAxisValues()

FEMdisplacement = FEMdispFile.getVariableData()
FEMpressure = FEMpresFile.getVariableData()
FEMyValues = FEMpresFile.getYAxisValues()

# Changing the Units (Pa->kPa, m->mm)  
for i in range ( EBFVMpresFile.getNumberOfPlottingCurves() ):
    EBFVMdisplacement[i] = EBFVMdisplacement[i]*1000
    EBFVMpressure[i] = EBFVMpressure[i]/1000
    FEMdisplacement[i] = FEMdisplacement[i]*1000
    FEMpressure[i] = FEMpressure[i]/1000
    
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
fig.suptitle('Displacement Profiles', fontsize=18, fontweight = 'bold')
axis = plt.subplot(111)

## Plotando dados (função loglog) e linhas de grade (função grid)
plt.grid( True, which='both', axis='both', linestyle = '-', color = '#B5B5B5' )
for i in range(numberOfCurves):
    if i == 0:
        eYValues = EBFVMyValues.copy()
        s.MySort( eYValues, EBFVMdisplacement[i]  )
        plt.plot( EBFVMdisplacement[i], eYValues,'s-', markerfacecolor='white',  markersize = 5, markeredgecolor = 'black', color = 'black',   label =   'EbFVM' )
        eYValues = FEMyValues.copy()
        s.MySort( eYValues, FEMdisplacement[i]  )
        plt.plot( FEMdisplacement[i], eYValues, '^-', markerfacecolor='white', markersize = 5, markeredgecolor = 'black', color = 'black',   label =  'FEM')
    else:
        eYValues = EBFVMyValues.copy()
        s.MySort( eYValues, EBFVMdisplacement[i]  )
        plt.plot( EBFVMdisplacement[i], eYValues,'s-', markerfacecolor='white', markersize = 5, markeredgecolor = 'black', color = 'black' )
        eYValues = FEMyValues.copy()
        s.MySort( eYValues, FEMdisplacement[i]  )
        plt.plot( FEMdisplacement[i], eYValues, '^-', markerfacecolor='white', markersize = 5, markeredgecolor = 'black', color = 'black')
    

## Mudando a posição e tamanho da área de plotagem
box = axis.get_position()
axis.set_position([box.x0+0.1, box.y0, box.width*0.7, box.height])

##Colocando informação do tempo
axis.annotate("t = 0 s",
            xy=(-0.6, 5), xycoords='data',
            xytext=(-0.45, 5.5), textcoords='data',
            arrowprops=dict(arrowstyle="->",
                            connectionstyle="arc3"),
            )

axis.annotate("t = 2000 s",
            xy=(-0.8, 4.3), xycoords='data',
            xytext=(-0.85, 3.5), textcoords='data',
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
plt.legend(loc = "lower right", numpoints = 1, fontsize = 12, frameon=True, title=r"\bf{Methods }" )
#plt.legend(loc = "upper left", numpoints = 1, fontsize = 12, frameon=False, title=r"\bf{Time levels}" )
plt.ylabel( r" y(m)", size = 14)
plt.xlabel( r" Vertical displacement(mm) ", size = 14) 

###plt.savefig('C:\\Users\\ggrbill\\Desktop\\figure1.pdf')
plt.show()

## Criando o gráfico
fig = plt.figure( num = 2, figsize = (10,6) )
fig.suptitle('Pressure Profiles', fontsize=18, fontweight = 'bold')
axis = plt.subplot(111)

## Plotando dados (função loglog) e linhas de grade (função grid)
plt.grid( True, which='both', axis='both', linestyle = '-', color = '#B5B5B5' )
for i in range(numberOfCurves):
    if i == 0:
        eYValues = EBFVMyValues.copy()
        s.MySort( eYValues, EBFVMpressure[i]  )
        plt.plot( EBFVMpressure[i], eYValues, 's-',  markerfacecolor='white', markersize = 5, markeredgecolor = 'black', color = 'black', label =  'EbFVM' )
        eYValues = FEMyValues.copy()
        s.MySort( eYValues, FEMpressure[i]  )
        plt.plot( FEMpressure[i], eYValues, '^-',  markerfacecolor='white', markersize = 5, markeredgecolor = 'black', color = 'black', label =  'FEM' )
    else:
        eYValues = EBFVMyValues.copy()
        s.MySort( eYValues, EBFVMpressure[i]  )
        plt.plot( EBFVMpressure[i], eYValues, 's-',  markerfacecolor='white', markersize = 5, markeredgecolor = 'black', color = 'black' )
        eYValues = FEMyValues.copy()
        s.MySort( eYValues, FEMpressure[i]  )
        plt.plot( FEMpressure[i], eYValues, '^-',  markerfacecolor='white', markersize = 5, markeredgecolor = 'black', color = 'black' )
       

## Mudando a posição e tamanho da área de plotagem
box = axis.get_position()
axis.set_position([box.x0+0.1, box.y0, box.width*0.7, box.height])

##Colocando informação do tempo
axis.annotate("t = 0 s",
            xy=(690, 5), xycoords='data',
            xytext=(610, 5.5), textcoords='data',
            arrowprops=dict(arrowstyle="->",
                            connectionstyle="arc3"),
            )

axis.annotate("t = 2000 s",
            xy=(150, 4.6), xycoords='data',
            xytext=(50, 3.5), textcoords='data',
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
plt.legend(loc = "lower left", numpoints = 1, fontsize = 12, frameon=True, title=r"\bf{Methods}" )
###plt.legend(loc = "upper right", numpoints = 1, fontsize = 12, frameon=False, title=r"\bf{Pressure}" )
plt.ylabel( r" y(m)", size = 14)
plt.xlabel( r" Pressure(kPa) ", size = 14) 

###plt.savefig('C:\\Users\\ggrbill\\Desktop\\figure2.pdf')
plt.show()
