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
import TriLogLog as tri

color_list = [  '#4F81BD', '#C0504D', '#9BBB59', '#8064A2', '#1F497D', '#F79646', '#953735', '#4F6228', '#984807' 
    , '#4F81BD', '#C0504D', '#9BBB59', '#8064A2', '#1F497D', '#F79646', '#953735', '#4F6228', '#984807'
    , '#4F81BD', '#C0504D', '#9BBB59', '#8064A2', '#1F497D', '#F79646', '#953735', '#4F6228', '#984807' ]

plt.close('all')

method = "FEM"

nDiv = 1
timeLevelsFiles = [50]
timeLevels = [50]
#timeSteps = ["0_05", "0_1", "0_25", "0_5", "1"]
#timeStepArray = ["0.05", "0.1", "0.25", "0.5", "1.0"]
#timeSteps = ["0_05", "0_25", "0_5", "1"]
#timeStepArray = ["0.05", "0.25", "0.5", "1.0"]

timeSteps = ["1", "0_5", "0_25", "0_1"]
timeStepArray = ["1.0", "0.5", "0.25", "0.1"]

timeStepInt = []
for i in range( len(timeStepArray) ):
    timeStepInt.append( float( timeStepArray[i] ) )
timeStepInt = np.array( timeStepInt )

grids = ["57", "228", "912", "3648"] #Hybrid
#grids = ["90", "360", "1440", "5760"] #Triangles

#grids = ["36", "81", "256", "784", "1936"] #Quadrangles
#grids = ["72", "162", "512", "1568", "3872"] #Triangles
#grids = ["144", "324", "1024", "3136", "7744"] #Triangles_2

## Lendo dados dos arquivos
xdisplacement = []
ydisplacement = []
pressure = []
stress = []
volumes = []
xValues = []
yValues = []
for i in range( len( timeSteps ) ) :
    xdisplacement.append( [] )
    ydisplacement.append( [] )
    pressure.append( [] )
    stress.append( [] )
    for j in range( len( grids ) ) :    
        xdispFile = reader.ReadEFVLibInspectorFile("Mandel_2_Convergence//Mandel_2_Dt_" + timeSteps[i]  + "_" + method + "//GridXDisplacement_" + grids[j] + ".csv", nDiv, timeLevelsFiles) 
        ydispFile = reader.ReadEFVLibInspectorFile("Mandel_2_Convergence//Mandel_2_Dt_" + timeSteps[i]  + "_" + method + "//GridYDisplacement_" + grids[j] + ".csv", nDiv, timeLevelsFiles) 
        presFile = reader.ReadEFVLibInspectorFile("Mandel_2_Convergence//Mandel_2_Dt_" + timeSteps[i]  + "_" + method + "//GridPressure_" + grids[j] + ".csv", nDiv, timeLevelsFiles) 
        strsFile = reader.ReadEFVLibInspectorFile("Mandel_2_Convergence//Mandel_2_Dt_" + timeSteps[i]  + "_" + method + "//GridStress_" + grids[j] + ".csv", nDiv, timeLevelsFiles)
        xdisplacement[i].append( xdispFile.getVariableData()[0] )
        ydisplacement[i].append( ydispFile.getVariableData()[0] )
        pressure[i].append( presFile.getVariableData()[0] )
        stress[i].append( strsFile.getVariableData()[0] )
        if i == 0 :
            xValues.append( xdispFile.getXAxisValues() )
            yValues.append( ydispFile.getYAxisValues() )
            volumes.append( presFile.getVolumeValues() )

## Calculando o comprimento característico da malha
h = []
for i in range( len(grids) ):
    h.append( 0 )
    for j in range( len( volumes[i] ) ):
        h[i] = h[i] + math.sqrt( volumes[i][j])
    h[i] =  h[i]/len( volumes[i] )

hs = []
for i in range( len(h) ):
    hs.append( str( "%.4f"%h[i] ) )

h = np.array( h )


biot = 0.7777777777777777777777777777777777777777777
## calculando a solução analitica
N = 200
                                    # lenght, height, F, permeability, phi, mi, K, K_s, K_f, G, K_phi 
#o = analytical.MandelsProblemAnalytical( 5.0, 5.0, 5.0e+7, 1.e-15, 0.19, 0.001, 8.0e+9, 3.6e+10, 3.3e+9, 6.0e+9, 3.6e+10 )
o = analytical.MandelsProblemAnalytical( 10.0, 2.0, 1.0e+4, 1.9e-15, 0.19, 0.001, 8.0e+9, 3.6e+10, 3.3e+9, 6.0e+9, 3.6e+10 )

anlPressure = []
anlStress = []
anlYDisplacement = []
anlXDisplacement = []
for i in range( len( grids ) ):
    anlPressure.append( [] )
    anlYDisplacement.append( [] )
    anlXDisplacement.append( [] )
    anlStress.append( [] )
    for j in range( len( volumes[i] ) ):
        if yValues[i][j] == 0.0:
            anlpress = o.getPressureValue( xValues[i][j] , timeLevels[0], 500 )
            anlPressure[i].append( anlpress )
            anlStress[i].append( o.getVertStressValue( xValues[i][j] , timeLevels[0], 500 )  + biot*anlpress )
            anlYDisplacement[i].append( o.getVertDisplacementValue( yValues[i][j] , timeLevels[0], 500 ) )
            anlXDisplacement[i].append( o.getHorDisplacementValue( xValues[i][j] , timeLevels[0], 500 ) )
        else:
            anlPressure[i].append( o.getPressureValue( xValues[i][j] , timeLevels[0], N ) )
            anlStress[i].append( o.getVertStressValue( xValues[i][j] , timeLevels[0], N ) + biot*anlPressure[i][j] )
            anlYDisplacement[i].append( o.getVertDisplacementValue( yValues[i][j] , timeLevels[0], N ) )
            anlXDisplacement[i].append( o.getHorDisplacementValue( xValues[i][j] , timeLevels[0], N ) )
    anlPressure[i] = np.array( anlPressure[i] )
    anlStress[i] = np.array( anlStress[i] )
    anlYDisplacement[i] = np.array( anlYDisplacement[i] )
    anlXDisplacement[i] = np.array( anlXDisplacement[i] )

## calculando o erro
presErro = []
ydispErro = []
xdispErro = []
stresErro = []

denErro = 0.0
numErro = 0.0
denErro1 = 0.0
numErro1 = 0.0
denErro2 = 0.0
numErro2 = 0.0
denErro3 = 0.0
numErro3 = 0.0
for i in range( len( timeSteps ) ):
    presErro.append( [] )
    ydispErro.append( [] )
    xdispErro.append( [] )
    stresErro.append( [] )
    for j in range( len( grids ) ):
        for k in range( len( volumes[j] ) ):
            numErro = numErro + ((pressure[i][j][k] - anlPressure[j][k])**2)*volumes[j][k] 
            denErro = denErro + (anlPressure[j][k]**2)*volumes[j][k] 
            numErro1 = numErro1 + ((ydisplacement[i][j][k] - anlYDisplacement[j][k])**2)*volumes[j][k] 
            denErro1 = denErro1 + (anlYDisplacement[j][k]**2)*volumes[j][k] 
            numErro2 = numErro2 + ((xdisplacement[i][j][k] - anlXDisplacement[j][k])**2)*volumes[j][k] 
            denErro2 = denErro2 + (anlXDisplacement[j][k]**2)*volumes[j][k] 
            numErro3 = numErro3 + ((stress[i][j][k] - anlStress[j][k])**2)*volumes[j][k] 
            denErro3 = denErro3 + (anlStress[j][k]**2)*volumes[j][k] 
            #print "Ts, Gd , Vl", i , j , k , ((displacement[i][j][k] - anlDisplacement[j][k])**2)*volumes[j][k], (anlDisplacement[j][k]**2)*volumes[j][k]
        #print numErro1, denErro1
        presErro[i].append( math.sqrt( numErro/denErro ) )
        ydispErro[i].append( math.sqrt( numErro1/denErro1 ) )
        xdispErro[i].append( math.sqrt( numErro2/denErro2 ) )
        stresErro[i].append( math.sqrt( numErro3/denErro3 ) )
        denErro = 0.0
        numErro = 0.0
        denErro1 = 0.0
        numErro1 = 0.0
        denErro2 = 0.0
        numErro2 = 0.0
        denErro3 = 0.0
        numErro3 = 0.0
    presErro[i] = np.array( presErro[i] )
    ydispErro[i] = np.array( ydispErro[i] )   
    xdispErro[i] = np.array( xdispErro[i] )   
    stresErro[i] = np.array( stresErro[i] )
   
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
X2, Y2, tl_x1, tl_y1, tl_x2, tl_y2 = tri.getLowerTri( -0.5, -4.0, 0.2, 2.0, 0.15 )
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
plt.legend( bbox_to_anchor = (1.02, 0.5), loc = "center left", numpoints = 1, fontsize = 12, frameon=False, title=r" $\Delta t$(s) " )
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
    plt.loglog( h, ydispErro[i], 'o-', color = color_list[i], markeredgecolor = color_list[i], linewidth = 0.95, label = str( timeStepArray[i] )  )

## Mudando a posição e tamanho da área de plotagem
box = axis.get_position()
axis.set_position([box.x0-0.03, box.y0+0.03, box.width*0.75, box.height])

## Adicionando triângulos
X2, Y2, tl_x1, tl_y1, tl_x2, tl_y2 = tri.getLowerTri( -0.5, -4.3, 0.2, 2.0, 0.15 )
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
plt.legend( bbox_to_anchor = (1.02, 0.5), loc = "center left", numpoints = 1, fontsize = 12, frameon=False, title=r" $\Delta t$(s) " )
plt.ylabel( r" Erro no deslocamento vertical", size = 16)
plt.xlabel( r" Comprimento caracter\'istico - $h$(m) ", size = 16) 

####plt.savefig('C:\\Users\\ggrbill\\Desktop\\figure1.pdf')
plt.show()



## Criando o gráfico
fig = plt.figure( num = 3, figsize = (8,5) )
axis = plt.subplot(111)

## Plotando dados (função loglog) e linhas de grade (função grid)
plt.grid( True, which='both', axis='both', linestyle = '-', color = '#B5B5B5' )
for i in range( len( timeSteps ) ):
    plt.loglog( h, xdispErro[i], 'o-', color = color_list[i], markeredgecolor = color_list[i], linewidth = 0.95, label = str( timeStepArray[i] )  )

## Mudando a posição e tamanho da área de plotagem
box = axis.get_position()
axis.set_position([box.x0-0.03, box.y0+0.03, box.width*0.75, box.height])

## Adicionando triângulos
X2, Y2, tl_x1, tl_y1, tl_x2, tl_y2 = tri.getLowerTri( -0.5, -4.3, 0.2, 2.0, 0.15 )
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
plt.legend( bbox_to_anchor = (1.02, 0.5), loc = "center left", numpoints = 1, fontsize = 12, frameon=False, title=r" $\Delta t$(s) " )
plt.ylabel( r" Erro no deslocamento horizontal", size = 16)
plt.xlabel( r" Comprimento caracter\'istico - $h$(m) ", size = 16) 

####plt.savefig('C:\\Users\\ggrbill\\Desktop\\figure1.pdf')
plt.show()



## Criando o gráfico
fig = plt.figure( num = 4, figsize = (8,5) )
axis = plt.subplot(111)

## Plotando dados (função loglog) e linhas de grade (função grid)
plt.grid( True, which='both', axis='both', linestyle = '-', color = '#B5B5B5' )
for i in range( len( timeSteps ) ):
    plt.loglog( h, stresErro[i], 'o-', color = color_list[i], markeredgecolor = color_list[i], linewidth = 0.95, label = str( timeStepArray[i] )  )

## Mudando a posição e tamanho da área de plotagem
box = axis.get_position()
axis.set_position([box.x0-0.03, box.y0+0.03, box.width*0.75, box.height])

## Adicionando triângulos
X2, Y2, tl_x1, tl_y1, tl_x2, tl_y2 = tri.getLowerTri( -0.5, -3.5, 0.2, 2.0, 0.15 )
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
plt.legend( bbox_to_anchor = (1.02, 0.5), loc = "center left", numpoints = 1, fontsize = 12, frameon=False, title=r" $\Delta t$(s) " )
plt.ylabel( r" Erro na tens\~ao vertical total", size = 16)
plt.xlabel( r" Comprimento caracter\'istico - $h$(m) ", size = 16) 

####plt.savefig('C:\\Users\\ggrbill\\Desktop\\figure1.pdf')
plt.show()


## Criando o gráfico
fig = plt.figure( num = 5, figsize = (8,5) )
axis = plt.subplot(111)

## Plotando dados (função loglog) e linhas de grade (função grid)
plt.grid( True, which='both', axis='both', linestyle = '-', color = '#B5B5B5' )
for i in range( len( h ) ):
    plt.loglog( timeStepInt, np.transpose( presErro )[i], 'o-', color = color_list[i], markeredgecolor = color_list[i], linewidth = 0.95, label = hs[i] )
    #plt.loglog( h, dispErro[i], '-', color = color_list[2], linewidth = 0.95, label = 'Vertical displacement error' )

## Mudando a posição e tamanho da área de plotagem
box = axis.get_position()
axis.set_position([box.x0-0.03, box.y0+0.03, box.width*0.75, box.height])

## Adicionando triângulos
X2, Y2, tl_x1, tl_y1, tl_x2, tl_y2 = tri.getLowerTri( -0.25, -3.7, 0.25, 1.0, 0.15 )
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
xMin, xMax = plt.xlim()
plt.xlim( 5.0e-2, 3.0e0 )
#yMin, yMax = plt.ylim()
#plt.ylim( 1.0e-6, 1.0e-3 ) 
#
### Configurando a legenda e os "labels" dos eixos - - -  bbox_to_anchor = (1.05, 0.5)
plt.legend( bbox_to_anchor = (1.02, 0.5), loc = "center left", numpoints = 1, fontsize = 12, frameon=False, title=r" $h$(m) " )
plt.ylabel( r" Erro na press\~ao", size = 16)
plt.xlabel( r" Passo de tempo - $\Delta t$(s) ", size = 16) 

####plt.savefig('C:\\Users\\ggrbill\\Desktop\\figure1.pdf')
plt.show()


## Criando o gráfico
fig = plt.figure( num = 6, figsize = (8,5) )
axis = plt.subplot(111)

## Plotando dados (função loglog) e linhas de grade (função grid)
plt.grid( True, which='both', axis='both', linestyle = '-', color = '#B5B5B5' )
for i in range( len( h ) ):
    plt.loglog( timeStepInt, np.transpose( ydispErro )[i], 'o-', color = color_list[i], markeredgecolor = color_list[i], linewidth = 0.95, label = hs[i]  )

## Mudando a posição e tamanho da área de plotagem
box = axis.get_position()
axis.set_position([box.x0-0.03, box.y0+0.03, box.width*0.75, box.height])

## Adicionando triângulos
X2, Y2, tl_x1, tl_y1, tl_x2, tl_y2 = tri.getLowerTri( -0.25, -5.0, 0.25, 1.0, 0.15 )
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
xMin, xMax = plt.xlim()
plt.xlim( 5.0e-2, 3.0e0 )
#yMin, yMax = plt.ylim()
#plt.ylim( 1.0e-6, 1.0e-3 ) 
#
### Configurando a legenda e os "labels" dos eixos - - -  bbox_to_anchor = (1.05, 0.5)
plt.legend( bbox_to_anchor = (1.02, 0.5), loc = "center left", numpoints = 1, fontsize = 12, frameon=False, title=r" $h$(m) " )
plt.ylabel( r" Erro no deslocamento vertical", size = 16)
plt.xlabel( r" Passo de tempo - $\Delta t$(s) ", size = 16) 

####plt.savefig('C:\\Users\\ggrbill\\Desktop\\figure1.pdf')
plt.show()

## Criando o gráfico
fig = plt.figure( num = 7, figsize = (8,5) )
axis = plt.subplot(111)

## Plotando dados (função loglog) e linhas de grade (função grid)
plt.grid( True, which='both', axis='both', linestyle = '-', color = '#B5B5B5' )
for i in range( len( h ) ):
    plt.loglog( timeStepInt, np.transpose( xdispErro )[i], 'o-', color = color_list[i], markeredgecolor = color_list[i], linewidth = 0.95, label = hs[i] )

## Mudando a posição e tamanho da área de plotagem
box = axis.get_position()
axis.set_position([box.x0-0.03, box.y0+0.03, box.width*0.75, box.height])

## Adicionando triângulos
X2, Y2, tl_x1, tl_y1, tl_x2, tl_y2 = tri.getLowerTri( -0.25, -4.9, 0.25, 1.0, 0.15 )
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
xMin, xMax = plt.xlim()
plt.xlim( 5.0e-2, 3.0e0 )
yMin, yMax = plt.ylim()
plt.ylim( 1.0e-6, 1.0e-3 ) 
#
### Configurando a legenda e os "labels" dos eixos - - -  bbox_to_anchor = (1.05, 0.5)
plt.legend( bbox_to_anchor = (1.02, 0.5), loc = "center left", numpoints = 1, fontsize = 12, frameon=False, title=r" $h$(m) " )
plt.ylabel( r" Erro no deslocamento horizontal", size = 16)
plt.xlabel( r" Passo de tempo - $\Delta t$(s) ", size = 16) 

####plt.savefig('C:\\Users\\ggrbill\\Desktop\\figure1.pdf')
plt.show()


## Criando o gráfico
fig = plt.figure( num = 8, figsize = (8,5) )
axis = plt.subplot(111)

## Plotando dados (função loglog) e linhas de grade (função grid)
plt.grid( True, which='both', axis='both', linestyle = '-', color = '#B5B5B5' )
for i in range( len( h ) ):
    plt.loglog( timeStepInt, np.transpose( stresErro )[i], 'o-', color = color_list[i], markeredgecolor = color_list[i], linewidth = 0.95, label = hs[i]  )

## Mudando a posição e tamanho da área de plotagem
box = axis.get_position()
axis.set_position([box.x0-0.03, box.y0+0.03, box.width*0.75, box.height])

## Adicionando triângulos
X2, Y2, tl_x1, tl_y1, tl_x2, tl_y2 = tri.getLowerTri( -0.25, -4.4, 0.25, 1.0, 0.15 )
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
xMin, xMax = plt.xlim()
plt.xlim( 5.0e-2, 3.0e0 )
#yMin, yMax = plt.ylim()
#plt.ylim( 1.0e-6, 1.0e-3 ) 
#
### Configurando a legenda e os "labels" dos eixos - - -  bbox_to_anchor = (1.05, 0.5)
plt.legend( bbox_to_anchor = (1.02, 0.5), loc = "center left", numpoints = 1, fontsize = 12, frameon=False, title=r" $h$(m) " )
plt.ylabel( r" Erro na tens\~ao vertical total", size = 16)
plt.xlabel( r" Passo de tempo - $\Delta t$(s) ", size = 16) 

####plt.savefig('C:\\Users\\ggrbill\\Desktop\\figure1.pdf')
plt.show()
