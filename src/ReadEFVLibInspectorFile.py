# -*- coding: utf-8 -*-
"""
Spyder Editor

This temporary script file is located here:
C:\Users\jurandir\.spyder2\.temp.py
"""

import numpy as np


class ReadEFVLibInspectorFile( object ):
    # Constructor -------------------------------------------------------------
    def __init__(self, FileLocation, numberOfDivisionForPlottingData = 1, timeLevelsList = None):
        self.__EFVLibInspectorFile = open(FileLocation);
        self.__nDiv = numberOfDivisionForPlottingData;
        self.__timeLevels = timeLevelsList
        
        self._Get_List();
        self._Get_Axis_Coordinates_And_Volumes();
        self._Number_of_Values();
        self._Number_of_Lines();
        self._Number_of_Points();
        self._Time_Levels_Existence();
        if self.__Error == False:
            self._Reading_File();        
        
    # Internal Function -------------------------------------------------------
    def _Get_List(self):
        self.__List = (self.__EFVLibInspectorFile).readlines();
        
    def _Get_Axis_Coordinates_And_Volumes(self):
        self.__XAxis = False
        self.__YAxis = False
        self.__ZAxis = False
        self.__VolumesExistence = False        
        for i in range(len(self.__List)):
            if self.__List[i] == 'Y Coordinates:\n':
                self.__YAxis = True
                self.__YDataLine = i +1;
            elif self.__List[i] == 'X Coordinates:\n':
                self.__XAxis = True
                self.__XDataLine = i + 1;
            elif self.__List[i] == 'Z Coordinates:\n':
                self.__ZAxis = True
                self.__ZDataLine = i +1;
            elif self.__List[i] == 'Volumes:\n':
                self.__VolumesExistence = True
                self.__VolumeDataLine = i + 1;
            elif self.__List[i] == '\n':
                #print i
                self.__DataLine = i + 2
                break;
                
    def _Number_of_Values(self):
        self.__NumberOfValues = len( self.__List[1].split(',') ) - 1;
    
    def _Number_of_Lines(self):
        self.__NumberOfLines = len(self.__List) - self.__DataLine
               
    def _Number_of_Points(self):
        if self.__timeLevels == None:
            self.__NumberOfPoints = int(self.__NumberOfLines/self.__nDiv)
        else:
            self.__NumberOfPoints = len(self.__timeLevels)
        
    def _Time_Levels_Existence(self):
        self.__Error=False
        if self.__timeLevels == None:
            self.__CurrentTime=[];        
            for i in range(self.__NumberOfPoints):            
                PointIndex = i*self.__nDiv;
                self.__CurrentTime.append( float( self.__List[self.__DataLine+PointIndex].split(',')[0]));
            self.__CurrentTime = np.array(self.__CurrentTime);
        else:
            TimeExistence = np.zeros((len(self.__timeLevels)),dtype=bool)
            self.__TimeLineData=[]
            for i in range(len(self.__timeLevels)):
                for j in range(self.__NumberOfLines):
                    if self.__timeLevels[i] + 0.00001 >= float( self.__List[self.__DataLine + j].split(',')[0]):
                        if self.__timeLevels[i] - 0.00001 <= float( self.__List[self.__DataLine + j].split(',')[0]):
                            TimeExistence[i] = True;
                            self.__TimeLineData.append(j)
                if TimeExistence[i] == False:
                    print 'Error: Time Level of ' + str(self.__timeLevels[i]) + ' doesn\'t exist.';
                    print 'File: ' + self.__EFVLibInspectorFile.name 
                    self.__Error=True
##                    break
            self.__CurrentTime = np.array( self.__timeLevels );
            
    def _Reading_File(self):
        if self.__YAxis == True:
            YAxisValues=[];
            for i in range(self.__NumberOfValues):
                YAxisValues.append( float( self.__List[self.__YDataLine].split(',')[i] ));
            self.__YAxisValues=np.array(YAxisValues)
        else:
            self.__YAxisValues = 'There isn\'t any Y axis'
        
        if self.__XAxis == True:
            XAxisValues=[];
            for i in range(self.__NumberOfValues):
                XAxisValues.append( float( self.__List[self.__XDataLine].split(',')[i] ));
            self.__XAxisValues=np.array(XAxisValues)
        else:
            self.__XAxisValues = 'There isn\'t any X axis'
            
        if self.__ZAxis == True:
            ZAxisValues=[];
            for i in range(self.__NumberOfValues):
                ZAxisValues.append( float( self.__List[self.__ZDataLine].split(',')[i] ));
            self.__ZAxisValues=np.array(ZAxisValues)
        else:
            self.__ZAxisValues = 'There isn\'t any Z axis'
        
        if self.__VolumesExistence == True:
            VolumeValues=[]
            for i in range(self.__NumberOfValues):
                VolumeValues.append( float( self.__List[self.__VolumeDataLine].split(',')[i] ));
            self.__VolumeValues = np.array(VolumeValues)
        else:
            self.__VolumeValues = 'There aren\'t any Volumes'
            
        VariableData=[]
        if self.__timeLevels == None:
            for i in range(self.__NumberOfPoints):
                PointIndex = i*self.__nDiv;
                VariableData.append( [] );
                for j in range(self.__NumberOfValues):
                    VariableData[i].append( float( self.__List[PointIndex+self.__DataLine].split(',')[j+1] ) )
            self.__VariableData = np.array(VariableData)
        else:
            for i in range(len(self.__timeLevels)):
                VariableData.append([]);
                for j in range(self.__NumberOfValues):
                    VariableData[i].append( float( self.__List[self.__DataLine + self.__TimeLineData[i]].split(',')[j+1]))
            self.__VariableData=np.array(VariableData)
            
        del self.__List;
            
        
                             
    # Class Interface ---------------------------------------------------------
    def getNumberOfPlottingCurves(self):
        return self.__NumberOfPoints;                             
                             
    def getYAxisValues (self):
        return self.__YAxisValues;
                   
    def getXAxisValues (self):
        return self.__XAxisValues;
        
    def getZAxisValues (self):
        return self.__ZAxisValues;
        
    def getVolumeValues (self):
        return self.__VolumeValues;
        
    def getCurrentTime (self):
        return self.__CurrentTime;
           
    def getVariableData (self):
        return self.__VariableData;

    def reorderData( self, coord ):
        '''Reorders all data according to coord.'''
        ct = 0
        while 1:
            ct += 1
            resp = 1
            for i in range( len(coord)-1 ):
                if coord[i] > coord[i+1]:
                    coord_i = coord[i]
                    coord[i] = coord[i+1]
                    coord[i+1] = coord_i
                    for listOfValues in self.__VariableData:
                        listOfValues_i = listOfValues[i]
                        listOfValues[i] = listOfValues[i+1]
                        listOfValues[i+1] = listOfValues_i
                    resp = 0                
            if resp == 1:
                    break






# EXAMPLE =======================================================================================

if __name__ == '__main__':
    timeLevels = [0,25,50]
    p = ReadEFVLibInspectorFile( "Terzaghi_2Regions_3_Dif_Mec_EBFVM//ColumnPressure_602.csv", 1, timeLevels )
    v = ReadEFVLibInspectorFile( "Terzaghi_2Regions_3_Dif_Mec_EBFVM//ColumnYDisplacement_602.csv", 1, timeLevels )
    print v.getYAxisValues()
    print v.getVariableData()[2]
    
    v.reorderData( v.getYAxisValues() )
    
    print '\n', v.getYAxisValues()
    print v.getVariableData()[2]

