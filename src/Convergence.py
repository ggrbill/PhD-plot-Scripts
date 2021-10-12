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
import TriLogLog as tri

plt.close('all')

color_list = [  '#4F81BD', '#C0504D', '#9BBB59', '#8064A2', '#1F497D', '#F79646', '#953735', '#4F6228', '#984807' 
    , '#4F81BD', '#C0504D', '#9BBB59', '#8064A2', '#1F497D', '#F79646', '#953735', '#4F6228', '#984807'
    , '#4F81BD', '#C0504D', '#9BBB59', '#8064A2', '#1F497D', '#F79646', '#953735', '#4F6228', '#984807' ]

#color_list = [ '#F79646', '#953735', '#4F6228', '#984807' ]
    
method = "EbFVM"

nDiv = 1
timeLevelsFile = [20]
timeLevels = [20]
timeSteps = ["1", "0_5", "0_25", "0_1", "0_05", "0_025" ]
timeStepArray = ["1.0", "0.5", "0.25", "0.1", "0.05", "0.025"]
#timeSteps = [ "1", "0_5", "0_25", "0_1", "0_05", "0_025", "0_01"]
#timeStepArray = [ "1.0", "0.5", "0.25", "0.1", "0.05", "0.025", "0.01"]
#timeSteps = [ "0_05", "0_1", "0_25", "0_5", "1"]
#timeStepArray = [ "0.05", "0.1", "0.25", "0.5", "1.0"]
#timeSteps = [ "1", "0_5", "0_25", "0_1", "0_05"]
#timeStepArray = [ "1.0", "0.5", "0.25", "0.1", "0.05"]

timeStepInt = []
for i in range( len(timeStepArray) ):
    timeStepInt.append( float( timeStepArray[i] ) )
timeStepInt = np.array( timeStepInt )

Mesh = "HYB"

text = ""
grids = []
if Mesh == "TRI"    :
    text = "_" + Mesh
    grids = ["48", "300", "1452", "2700", "5292" ]
if Mesh == "HYB"    :
    grids = ["91", "364", "1456", "5824"]
if Mesh == "QUAD"    :
    text = "_" + Mesh
    grids = ["24", "150", "726", "1350", "2646" ]

#grids = ["46", "91", "155", "168", "306", "602"]
#grids = ["306", "1224", "4896", "19584"]
#grids = ["24", "54", "150", "294", "726", "2646" ]
#grids = ["24", "150", "726", "1350", "2646" ]
#grids = ["96", "216", "600", "1176", "2904", "10584" ]
#grids = ["24", "54", "96", "150", "216", "294", "726", "1350", "2646", "6936"]
#grids = ["48", "108", "300", "588", "1452", "5292"]



## Lendo dados dos arquivos

displacement = []
pressure = []
volumes = []
yValues = []
for i in range( len( timeSteps ) ) :
    displacement.append( [] )
    pressure.append( [] )
    for j in range( len( grids ) ) :    
        dispFile = reader.ReadEFVLibInspectorFile("Terzaghi_6_Convergence" + text + "//Conv_Terzaghi_6_Dt_" + timeSteps[i]  + "_" + method + "//GridYDisplacement_" + grids[j] + ".csv", nDiv, timeLevelsFile) 
        presFile = reader.ReadEFVLibInspectorFile("Terzaghi_6_Convergence" + text + "//Conv_Terzaghi_6_Dt_" + timeSteps[i]  + "_" + method + "//GridPressure_" + grids[j] + ".csv", nDiv, timeLevelsFile) 
        #dispFile = reader.ReadEFVLibInspectorFile("Terzaghi_6_Dt_" + timeSteps[i]  + "_" + method + "//GridYDisplacement_" + grids[j] + ".csv", nDiv, timeLevelsFile) 
        #presFile = reader.ReadEFVLibInspectorFile("Terzaghi_6_Dt_" + timeSteps[i]  + "_" + method + "//GridPressure_" + grids[j] + ".csv", nDiv, timeLevelsFile) 
        displacement[i].append( dispFile.getVariableData()[0] )
        pressure[i].append( presFile.getVariableData()[0] )
        if i == 0 :
            yValues.append( presFile.getYAxisValues() )
            volumes.append( presFile.getVolumeValues() )

## Calculando o comprimento característico da malha
h = []
for i in range( len(grids) ):
    h.append( 0 )
    for j in range( len( volumes[i] ) ):
        h[i] = h[i] + math.sqrt( volumes[i][j] )
    h[i] =  h[i]/len( volumes[i] )

hs = []
for i in range( len(h) ):
    hs.append( str( "%.4f"%h[i] ) )

h = np.array( h )
## calculando a solução analitica
N = 300


#                                        height, tao_0, permeability, phi, mi,    K,      K_s,     K_f,    G,     K_phi
o = analytical.TerzaghisProblemAnalytical( 6.0, 1.0e+6, 1.9e-15, 0.19, 0.001, 8.0e+9, 3.6e+10, 3.3e+9, 6.0e+9, 3.6e+10 ) #Berea
#o = analytical.TerzaghisProblemAnalytical( 6.0, 1.0e+6, 5.6e-15, 0.19, 0.001, 8.4e+9, 3.1e+10, 3.3e+9, 6.8e+9, 3.1e+10 ) #Ohio
#o = analytical.TerzaghisProblemAnalytical( 6.0, 1.0e+6, 8.0e-16, 0.20, 0.001, 6.7e+9, 3.9e+10, 3.3e+9, 5.9e+9, 3.9e+10 ) #Pecos
#o = analytical.TerzaghisProblemAnalytical( 6.0, 1.0e+6, 2.0e-16, 0.02, 0.001, 1.3e+10, 3.6e+10, 3.3e+9, 1.3e+10, 3.6e+10 ) #Ruhr
#o = analytical.TerzaghisProblemAnalytical( 6.0, 1.0e+6, 1.0e-15, 0.06, 0.001, 1.3e+10, 3.6e+10, 3.3e+9, 1.2e+10, 3.6e+10 ) #Weber

anlPressure = []
anlDisplacement = []
for i in range( len( grids ) ):
    anlPressure.append( [] )
    anlDisplacement.append( [] )
    for j in range( len( volumes[i] ) ):
        if yValues[i][j] == 0.0:
            anlPressure[i].append( o.getPressureValue( yValues[i][j] , timeLevels[0], 300 ) )
            anlDisplacement[i].append( o.getDisplacementValue( yValues[i][j] , timeLevels[0], 300 ) )
        else:
            anlPressure[i].append( o.getPressureValue( yValues[i][j] , timeLevels[0], N ) )
            anlDisplacement[i].append( o.getDisplacementValue( yValues[i][j] , timeLevels[0], N ) )
    anlPressure[i] = np.array( anlPressure[i] )
    anlDisplacement[i] = np.array( anlDisplacement[i] )

## calculando o erro
presErro = []
dispErro = []

denErro = 0.0
numErro = 0.0
denErro1 = 0.0
numErro1 = 0.0

## norma L2 do Erro
for i in range( len( timeSteps ) ):
    presErro.append( [] )
    dispErro.append( [] )
    for j in range( len( grids ) ):
        for k in range( len( volumes[j] ) ):
            numErro = numErro + ((pressure[i][j][k] - anlPressure[j][k])**2)*volumes[j][k] 
            denErro = denErro + (anlPressure[j][k]**2)*volumes[j][k] 
            numErro1 = numErro1 + ((displacement[i][j][k] - anlDisplacement[j][k])**2)*volumes[j][k] 
            denErro1 = denErro1 + (anlDisplacement[j][k]**2)*volumes[j][k] 
            #print "Ts, Gd , Vl", i , j , k , ((displacement[i][j][k] - anlDisplacement[j][k])**2)*volumes[j][k], (anlDisplacement[j][k]**2)*volumes[j][k]
        #print numErro1, denErro1
        pErro = math.sqrt( numErro/denErro )
        dErro = math.sqrt( numErro1/denErro1 )
        presErro[i].append( pErro )
        dispErro[i].append( dErro )
        denErro = 0.0
        numErro = 0.0
        denErro1 = 0.0
        numErro1 = 0.0
    presErro[i] = np.array( presErro[i] )
    dispErro[i] = np.array( dispErro[i] )   
  
## Norma L_inf  do Erro
#for i in range( len( timeSteps ) ):
#    presErro.append( [] )
#    dispErro.append( [] )
#    for j in range( len( grids ) ):
#        for k in range( len( volumes[j] ) ):
#            if numErro <= math.fabs(pressure[i][j][k] - anlPressure[j][k]) :
#                numErro = math.fabs(pressure[i][j][k] - anlPressure[j][k])
#            if denErro <= math.fabs(anlPressure[j][k])  :
#                denErro = math.fabs(anlPressure[j][k]) 
#            if numErro1 <= math.fabs(displacement[i][j][k] - anlDisplacement[j][k]) :
#                numErro1 = math.fabs(displacement[i][j][k] - anlDisplacement[j][k])
#            if denErro1 <= math.fabs(anlDisplacement[j][k]) :
#                denErro1 = math.fabs(anlDisplacement[j][k]) 
#            #print "Ts, Gd , Vl", i , j , k , ((displacement[i][j][k] - anlDisplacement[j][k])**2)*volumes[j][k], (anlDisplacement[j][k]**2)*volumes[j][k]
#        #print numErro1, denErro1
#        presErro[i].append( math.sqrt( numErro/denErro ) )
#        dispErro[i].append( math.sqrt( numErro1/denErro1 ) )
#        denErro = 0.0
#        numErro = 0.0
#        denErro1 = 0.0
#        numErro1 = 0.0
#    presErro[i] = np.array( presErro[i] )
#    dispErro[i] = np.array( dispErro[i] )   
   
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
fig = plt.figure( num = 1, figsize = (8,5) )
axis = plt.subplot(111)

## Plotando dados (função loglog) e linhas de grade (função grid)
plt.grid( True, which='both', axis='both', linestyle = '-', color = '#B5B5B5' )
for i in range( len( timeSteps ) ):
    plt.loglog( h, presErro[i], 'o-', color = color_list[i], markeredgecolor = color_list[i], linewidth = 0.95, label = str( timeStepArray[i] ) )
    #plt.loglog( h, dispErro[i], '-', color = color_list[2], linewidth = 0.95, label = 'Vertical displacement error' )

## Mudando a posição e tamanho da área de plotagem
box = axis.get_position()
axis.set_position([box.x0-0.03, box.y0+0.03, box.width*0.75, box.height])

## Adicionando triângulos
if Mesh == "HYB":
    X2, Y2, tl_x1, tl_y1, tl_x2, tl_y2 = tri.getLowerTri( -0.8, -3.7, 0.2, 2.0, 0.15 )
if Mesh == "TRI":
    X2, Y2, tl_x1, tl_y1, tl_x2, tl_y2 = tri.getLowerTri( -0.6, -3.7, 0.2, 2.0, 0.15 )
if Mesh == "QUAD":
    X2, Y2, tl_x1, tl_y1, tl_x2, tl_y2 = tri.getLowerTri( -0.6, -4.6, 0.2, 2.0, 0.15 )

for x2, y2 in zip( X2, Y2 ):
    plt.loglog( x2, y2, '-', color='black' )
plt.text( tl_x1, tl_y1, '1.0' )
plt.text( tl_x2, tl_y2, '2.0' )

## linhas de grade posicionadas atrás das curvas plotadas
axis.set_axisbelow( True )
## Invertendo direção do Eixo X
#axis.invert_xaxis()

### Tamanho da fonte dos "labels" dos marcadores (ticks)
plt.tick_params( axis='both', which='major', labelsize=10) 

### Limites dos eixos
#xMin, xMax = plt.xlim()
#plt.xlim( 1e-2, 1e0 )
#yMin, yMax = plt.ylim()
#plt.ylim( 1.0e-5, 1.0e-2 ) 
#
### Configurando a legenda e os "labels" dos eixos - - -  bbox_to_anchor = (1.05, 0.5)
#plt.legend( loc = "upper right", numpoints = 1, fontsize = 12, frameon=True, title=r" $\Delta t$ ", fancybox=True, borderpad=1, labelspacing=0.5 )
plt.legend( bbox_to_anchor = (1.02, 0.5), loc = "center left", numpoints = 1, fontsize = 12, frameon=False, title=r" $\Delta t$ (s) " ) #, fancybox=True, borderpad=1, labelspacing=0.5 )
plt.ylabel( r" Erro na press\~ao", size = 16)
plt.xlabel( r" Comprimento caracter\'istico - $h$(m) ", size = 16) 

####plt.savefig('C:\\Users\\ggrbill\\Desktop\\figure1.pdf')
plt.show()



## Criando o gráfico
fig = plt.figure( num = 2, figsize = (8,5) )
axis = plt.subplot(111)

## Plotando dados (função loglog) e linhas de grade (função grid)
plt.grid( True, which='both', axis='both', linestyle = '-', color = '#B5B5B5' )
for i in range( len( timeSteps ) ):
    plt.loglog( h, dispErro[i], 'o-', color = color_list[i], markeredgecolor = color_list[i], linewidth = 0.95, label = str( timeStepArray[i] )  )

## Mudando a posição e tamanho da área de plotagem
box = axis.get_position()
axis.set_position([box.x0-0.03, box.y0+0.03, box.width*0.75, box.height])

## Adicionando triângulos
if Mesh == "HYB":
    X2, Y2, tl_x1, tl_y1, tl_x2, tl_y2 = tri.getLowerTri( -0.8, -4.5, 0.2, 2.0, 0.15 )
if Mesh == "TRI":
    X2, Y2, tl_x1, tl_y1, tl_x2, tl_y2 = tri.getLowerTri( -0.6, -3.8, 0.2, 2.0, 0.15 )
if Mesh == "QUAD":
    X2, Y2, tl_x1, tl_y1, tl_x2, tl_y2 = tri.getLowerTri( -0.6, -3.9, 0.2, 2.0, 0.20 )

for x2, y2 in zip( X2, Y2 ):
    plt.loglog( x2, y2, '-', color='black' )
plt.text( tl_x1, tl_y1, '1.0' )
plt.text( tl_x2, tl_y2, '2.0' )

## linhas de grade posicionadas atrás das curvas plotadas
axis.set_axisbelow( True )
## Invertendo direção do Eixo X
#axis.invert_xaxis()

### Tamanho da fonte dos "labels" dos marcadores (ticks)
plt.tick_params( axis='both', which='major', labelsize=10) 
#
### Configurando a legenda e os "labels" dos eixos - - -  bbox_to_anchor = (1.05, 0.5)
#plt.legend(loc = "upper right", numpoints = 1, fontsize = 12, frameon=True, title=r" $\Delta t$ ", fancybox=True, borderpad=1, labelspacing=0.5 )
plt.legend( bbox_to_anchor = (1.02, 0.5), loc = "center left", numpoints = 1, fontsize = 12, frameon=False, title=r" $\Delta t$ (s) " ) #, fancybox=True, borderpad=1, labelspacing=0.5 )
plt.ylabel( r" Erro no deslocamento", size = 16)
plt.xlabel( r" Comprimento caracter\'istico - $h$(m) ", size = 16) 

####plt.savefig('C:\\Users\\ggrbill\\Desktop\\figure1.pdf')
plt.show()


## Criando o gráfico
fig = plt.figure( num = 3, figsize = (8,5) )
axis = plt.subplot(111)

## Plotando dados (função loglog) e linhas de grade (função grid)
plt.grid( True, which='both', axis='both', linestyle = '-', color = '#B5B5B5' )
for i in range( len( hs ) ):
    plt.loglog( timeStepInt, np.transpose( dispErro )[i], 'o-', color = color_list[i], markeredgecolor = color_list[i], linewidth = 0.95, label = hs[i] )

## Mudando a posição e tamanho da área de plotagem
box = axis.get_position()
axis.set_position([box.x0-0.03, box.y0+0.03, box.width*0.75, box.height])

## Adicionando triângulos
if Mesh == "HYB":
    X2, Y2, tl_x1, tl_y1, tl_x2, tl_y2 = tri.getLowerTri( -0.25, -4.5, 0.3, 1.0, 0.15 )
if Mesh == "TRI":
    X2, Y2, tl_x1, tl_y1, tl_x2, tl_y2 = tri.getLowerTri( -0.25, -4.5, 0.3, 1.0, 0.15 )
if Mesh == "QUAD":
    X2, Y2, tl_x1, tl_y1, tl_x2, tl_y2 = tri.getLowerTri( -0.25, -4.5, 0.3, 1.0, 0.2 )
    
for x2, y2 in zip( X2, Y2 ):
    plt.loglog( x2, y2, '-', color='black' )
plt.text( tl_x1, tl_y1, '1.0' )
plt.text( tl_x2, tl_y2, '1.0' )

## linhas de grade posicionadas atrás das curvas plotadas
axis.set_axisbelow( True )
## Invertendo direção do Eixo X
#axis.invert_xaxis()

### Tamanho da fonte dos "labels" dos marcadores (ticks)
plt.tick_params( axis='both', which='major', labelsize=10) 

### Limites dos eixos
#xMin, xMax = plt.xlim()
#plt.xlim( 1.0e-2, 1.0e1 )
#yMin, yMax = plt.ylim()
#plt.ylim( 1.0e-6, 1.0e-3 ) 
#
### Configurando a legenda e os "labels" dos eixos - - -  bbox_to_anchor = (1.05, 0.5)
# plt.legend(loc = "lower right", numpoints = 1, fontsize = 12, frameon=True, title=r" $h$ ", fancybox=True, borderpad=1, labelspacing=0.5 )
plt.legend( bbox_to_anchor = (1.02, 0.5), loc = "center left", numpoints = 1, fontsize = 12, frameon=False, title=r" $h$(m) " ) #, fancybox=True, borderpad=1, labelspacing=0.5 )
plt.ylabel( r" Erro no deslocamento", size = 16)
plt.xlabel( r" Passo de tempo - $\Delta t$(s) ", size = 16) 

####plt.savefig('C:\\Users\\ggrbill\\Desktop\\figure1.pdf')
plt.show()


## Criando o gráfico
fig = plt.figure( num = 4, figsize = (8,5) )
axis = plt.subplot(111)

## Plotando dados (função loglog) e linhas de grade (função grid)
plt.grid( True, which='both', axis='both', linestyle = '-', color = '#B5B5B5' )
for i in range( len( hs ) ):
    plt.loglog( timeStepInt, np.transpose( presErro )[i], 'o-', color = color_list[i], markeredgecolor = color_list[i], linewidth = 0.95, label = hs[i] )

## Mudando a posição e tamanho da área de plotagem
box = axis.get_position()
axis.set_position([box.x0-0.03, box.y0+0.03, box.width*0.75, box.height])

## Adicionando triângulos
if Mesh == "HYB":
    X2, Y2, tl_x1, tl_y1, tl_x2, tl_y2 = tri.getLowerTri( -0.25, -3.2, 0.3, 1.0, 0.15 )
if Mesh == "TRI":
    X2, Y2, tl_x1, tl_y1, tl_x2, tl_y2 = tri.getLowerTri( -0.25, -3.0, 0.3, 1.0, 0.15 )
if Mesh == "QUAD":
    X2, Y2, tl_x1, tl_y1, tl_x2, tl_y2 = tri.getLowerTri( -0.25, -3.2, 0.3, 1.0, 0.15 )
    
for x2, y2 in zip( X2, Y2 ):
    plt.loglog( x2, y2, '-', color='black' )
plt.text( tl_x1, tl_y1, '1.0' )
plt.text( tl_x2, tl_y2, '1.0' )

## linhas de grade posicionadas atrás das curvas plotadas
axis.set_axisbelow( True )
## Invertendo direção do Eixo X
#axis.invert_xaxis()

### Tamanho da fonte dos "labels" dos marcadores (ticks)
plt.tick_params( axis='both', which='major', labelsize=10) 

### Limites dos eixos
#xMin, xMax = plt.xlim()
#plt.xlim( 1e-2, 1e1 )
#yMin, yMax = plt.ylim()
#plt.ylim( 1.0e-5, 1.0e-2 ) 
#
### Configurando a legenda e os "labels" dos eixos - - -  bbox_to_anchor = (1.05, 0.5)
# plt.legend(loc = "lower right", numpoints = 1, fontsize = 12, frameon=True, title=r" $h$ ", fancybox=True, borderpad=1, labelspacing=0.5 )
plt.legend( bbox_to_anchor =(1.02, 0.5), loc = "center left", numpoints = 1, fontsize = 12, frameon=False, title=r" $h$(m)") #, fancybox=True, borderpad=1, labelspacing=0.5 )
plt.ylabel( r" Erro na press\~ao", size = 16)
plt.xlabel( r" Passo de tempo - $\Delta t$(s) ", size = 16) 

####plt.savefig('C:\\Users\\ggrbill\\Desktop\\figure1.pdf')
plt.show()

################# Gráfico de Acompanhamento do Deslocamento #################
#nGrids = len( grids )
#numTopDisp = []
#anlTopDisp = []
#for i in range( nGrids ):
#    numTopDisp.append( displacement[0][i][0]*1000 )
#    anlTopDisp.append( anlDisplacement[i][0]*1000 )
#    
### Criando o gráfico
#fig = plt.figure( num = 5, figsize = (8,5) )
#axis = plt.subplot(111)
#
## Plotando dados (função loglog) e linhas de grade (função grid)
#plt.grid( True, which='both', axis='both', linestyle = '-', color = '#B5B5B5' )
#plt.plot( h, numTopDisp, 'o-', markeredgecolor = color_list[0], markersize = 4, color = color_list[0], label = r"Num\'erica" )
#plt.plot( h, anlTopDisp, '-', color = 'black', label = r"Anal\'{\i}tica" )
#
### Mudando a posição e tamanho da área de plotagem
#box = axis.get_position()
#axis.set_position([box.x0-0.03, box.y0+0.03, box.width*0.75, box.height])
#
### linhas de grade posicionadas atrás das curvas plotadas
#axis.set_axisbelow( True )
### Invertendo direção do Eixo X
##axis.invert_xaxis()
#
#### Tamanho da fonte dos "labels" dos marcadores (ticks)
#plt.tick_params( axis='both', which='major', labelsize=10) 
#
#### Limites dos eixos
##xMin, xMax = plt.xlim()
##plt.xlim( 1e-2, 1e1 )
#yMin, yMax = plt.ylim()
#plt.ylim( -2.63e-4, -2.61e-4 ) 
#
#### Configurando a legenda e os "labels" dos eixos - - -  bbox_to_anchor = (1.05, 0.5)
#plt.legend( bbox_to_anchor =(1.02, 0.5), loc = "center left", numpoints = 1, fontsize = 12, frameon=False, title= r"\bf{Solu\c{c}\~ao}" ) #, fancybox=True, borderpad=1, labelspacing=0.5 )
#plt.ylabel( r" Deslocamento no topo da coluna (mm)", size = 16)
#plt.xlabel( r" Comprimento caracter\'istico - $h$(m) ", size = 16) 