# -*- coding: cp1252 -*-
"""
Created on Sun Jan 25 18:32:50 2015

@author: ggrbill
"""
import numpy as np
import math
import TwoLayeredSoilAnalytical as analytical
import ReadEFVLibInspectorFile as reader

color_list = [  '#4F81BD', '#C0504D', '#9BBB59', '#8064A2', '#1F497D', '#F79646', '#953735', '#4F6228', '#984807' 
    , '#4F81BD', '#C0504D', '#9BBB59', '#8064A2', '#1F497D', '#F79646', '#953735', '#4F6228', '#984807'
    , '#4F81BD', '#C0504D', '#9BBB59', '#8064A2', '#1F497D', '#F79646', '#953735', '#4F6228', '#984807' ]

nDiv = 4;
timeLevels = [25,50]
presFile = reader.ReadEFVLibInspectorFile("Terzaghi_2Regions_0_Rk_10_EBFVM//GridPressure_155.csv", nDiv, timeLevels)
factor = 10.

#presFile = open("Terzaghi_2Regions_1_Rk_100//GridPressure_155.csv")
#factor = 100.

#presFile = open("Terzaghi_2Regions_2_Rk_0_1//GridPressure_155.csv")
#factor = 0.1

currentTime = presFile.getCurrentTime()
pressure = presFile.getVariableData()
yValues = presFile.getYAxisValues()
volumes = presFile.getVolumeValues()

infPerm = 1.9e-15
supPerm = factor * infPerm

## Calculando o comprimento característico da malha
h = 0
for i in range( len(volumes) ):
    h = h + volumes[i]
   
h = math.sqrt(h)/len( volumes )

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
    anlPressure.append( [] )
    for j in range( len( volumes ) ):
        anlPressure[i].append( o.getPressureValue( yValues[j] , anlCurrentTime[i], N ) )
    anlPressure[i] = np.array(anlPressure[i])

## calculando o erro
presErro = []
denErro = 0.0
numErro = 0.0
for i in range( presFile.getNumberOfPlottingCurves() ):
    for j in range( len( volumes ) ):
        numErro = numErro + ((pressure[i][j]- anlPressure[i][j])**2)*volumes[j] 
        denErro = denErro + (anlPressure[i][j]**2)*volumes[j] 
    presErro.append( math.sqrt( numErro/denErro ) )
    denErro = 0.0
    numErro = 0.0        