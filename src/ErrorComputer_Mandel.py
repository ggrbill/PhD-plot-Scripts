# -*- coding: cp1252 -*-
"""
Created on Sun Jan 25 18:32:50 2015

@author: ggrbill
"""
import numpy as np
import math
import matplotlib
import matplotlib.pyplot as plt
import MandelsProblemAnalytical as analytical
import ReadEFVLibInspectorFile as reader

color_list = [  '#4F81BD', '#C0504D', '#9BBB59', '#8064A2', '#1F497D', '#F79646', '#953735', '#4F6228', '#984807' 
    , '#4F81BD', '#C0504D', '#9BBB59', '#8064A2', '#1F497D', '#F79646', '#953735', '#4F6228', '#984807'
    , '#4F81BD', '#C0504D', '#9BBB59', '#8064A2', '#1F497D', '#F79646', '#953735', '#4F6228', '#984807' ]


nDiv = 5;
timeLevels = [25,50,100]
dispFile = reader.ReadEFVLibInspectorFile("Mandel_2_dt_0_1_EbFVM//gridYDisplacement_153.csv", nDiv, timeLevels)
xdispFile = reader.ReadEFVLibInspectorFile("Mandel_2_dt_0_1_EbFVM//gridXDisplacement_153.csv", nDiv, timeLevels)
presFile = reader.ReadEFVLibInspectorFile("Mandel_2_dt_0_1_EbFVM//GridPressure_153.csv", nDiv, timeLevels)
stresFile = reader.ReadEFVLibInspectorFile("Mandel_2_dt_0_1_EbFVM//GridStress_153.csv", nDiv, timeLevels)


currentTime = dispFile.getCurrentTime()
vDisplacement = dispFile.getVariableData()
yValues = dispFile.getYAxisValues()
uDisplacement = xdispFile.getVariableData()
pressure = presFile.getVariableData()
stress = stresFile.getVariableData()
xValues = presFile.getXAxisValues()
volumes = presFile.getVolumeValues()

biot = 0.7777777777777777777777777777777777777777777

## Calculando o comprimento característico da malha
h = 0
for i in range( len(volumes) ):
    h = h + volumes[i]
   
h = math.sqrt(h)/len( volumes )

anlCurrentTime = currentTime
anlvDisplacement = []
anluDisplacement = []
anlPressure = []
anlStress = []

## calculando a solução analitica
N = 200
# lenght, height, F, permeability, phi, mi, K, K_s, K_f, G, K_phi 
o = analytical.MandelsProblemAnalytical( 10.0, 2.0, 1.0e+4, 1.9e-15, 0.19, 0.001, 8.0e+9, 3.6e+10, 3.3e+9, 6.0e+9, 3.6e+10 )
for i in range( presFile.getNumberOfPlottingCurves() ):
    anlvDisplacement.append( [] )
    anluDisplacement.append( [] )
    anlPressure.append( [] )
    anlStress.append( [] )
    for j in range( len( volumes ) ):
        anlvDisplacement[i].append( o.getVertDisplacementValue( yValues[j] , anlCurrentTime[i], N ) )
        anluDisplacement[i].append( o.getHorDisplacementValue( xValues[j] , anlCurrentTime[i], N ) )
        if xValues[j] == 10.0:
            anlPressure[i].append( 0.0 )
        else:
            anlPressure[i].append( o.getPressureValue( xValues[j] , anlCurrentTime[i], N ) )
        anlStress[i].append( o.getVertStressValue( xValues[j] , anlCurrentTime[i], N ) + biot*anlPressure[i][j] )
    anlvDisplacement[i] = np.array(anlvDisplacement[i])
    anluDisplacement[i] = np.array(anluDisplacement[i])
    anlPressure[i] = np.array(anlPressure[i])
    anlStress[i] = np.array(anlStress[i])
    
## calculando o erro
presErro = []
dispErro = []
udispErro = []
stressErro = []

denErro = 0.0
numErro = 0.0
denErro1 = 0.0
numErro1 = 0.0
denErro2 = 0.0
numErro2 = 0.0
denErro3 = 0.0
numErro3 = 0.0
for i in range( presFile.getNumberOfPlottingCurves() ):
    for j in range( len( volumes ) ):
        numErro = numErro + ((pressure[i][j]- anlPressure[i][j])**2)*volumes[j] 
        denErro = denErro + (anlPressure[i][j]**2)*volumes[j] 
        numErro1 = numErro1 + ((vDisplacement[i][j]- anlvDisplacement[i][j])**2)*volumes[j] 
        denErro1 = denErro1 + (anlvDisplacement[i][j]**2)*volumes[j]
        numErro2 = numErro2 + ((uDisplacement[i][j]- anluDisplacement[i][j])**2)*volumes[j] 
        denErro2 = denErro2 + (anluDisplacement[i][j]**2)*volumes[j]
        numErro3 = numErro3 + ((stress[i][j]- anlStress[i][j])**2)*volumes[j] 
        denErro3 = denErro3 + (anlStress[i][j]**2)*volumes[j]
    presErro.append( math.sqrt( numErro/denErro ) )
    dispErro.append( math.sqrt( numErro1/denErro1 ) )
    udispErro.append( math.sqrt( numErro2/denErro2 ) )
    stressErro.append( math.sqrt( numErro3/denErro3 ) )
    denErro = 0.0
    numErro = 0.0
    denErro1 = 0.0
    numErro1 = 0.0
    denErro2 = 0.0
    numErro2 = 0.0
    denErro3 = 0.0
    numErro3 = 0.0
        
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
plt.plot( anlCurrentTime, udispErro, '-', color = color_list[3], linewidth = 0.95, label = 'Horizontal displacement error' )
plt.plot( anlCurrentTime, stressErro, '-', color = color_list[4], linewidth = 0.95, label = 'Vertical stress error' )

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