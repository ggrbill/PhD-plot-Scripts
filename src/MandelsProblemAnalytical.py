# -*- coding: cp1252 -*-
# ABREVIATIONS USED =============================================================================

# ny - Number of points in the y direction
# nx - Number of points in the x direction
# lenght - Domain lenght
# height - Domain height
# F - Force applied in the north boundary
# permeability - Reference permeability
# phi - Reference porosity
# mi - Viscosity
# K - Bulk modulus
# K_s - Solid bulk modulus
# K_f - Fluid bulk modulus
# G - Sheer modulus
# K_phi - Unjacket pore compressibility

# H - Poroelastic expansion coefficient
# R - Biot modulus
# alpha - Biot-Willis coefficient
# K_p - Drained pore compressibility
# K_u - Undrained bulk modulus
# B - Skempton's coefficient
# ni - Drained Poisson's ratio
# ni_u - Undrained Poisson's ratio
# K_ni_u - Uniaxial undrained bulk modulus
# c_s - Solid phase compressibility
# c_f - Fluid phase compressibility
# gama - Loading efficiency
# c - Consolidation coefficient / Hydraulic diffusivity


import math;


# CLASS DEFINITION ==============================================================================

class MandelsProblemAnalytical( object ):

        # Constructor ---------------------------------------------------------------------------
        def __init__( self, lenght, height, F, permeability, phi, mi, K, K_s, K_f, G, K_phi ):
                self.lenght = lenght;
                self.height = height;
                self.F = F;
                self.permeability = permeability;
                self.phi = phi;
                self.mi = mi;
                self.K = K;
                self.K_s = K_s;
                self.K_f = K_f;
                self.G = G;
                self.K_phi = K_phi;

                self._calculate_H();
                self._calculate_R();
                self._calculate_alpha();
                self._calculate_K_p();
                self._calculate_B();
                self._calculate_K_u();
                self._calculate_ni();
                self._calculate_ni_u();
                self._calculate_K_ni_u();
                self._calculate_c_s();
                self._calculate_c_f();
                self._calculate_gama();
                self._calculate_c();
                

        # Internal functions --------------------------------------------------------------------
        def _calculate_H( self ):
                self.H = 1.0 / ( ( 1.0 / self.K ) - ( 1.0 / self.K_s ) );

        def _calculate_R( self ):
                self.R = 1.0 / ( ( 1.0 / self.H ) + self.phi * ( ( 1.0 / self.K_f ) - ( 1.0 / self.K_phi ) ) );

        def _calculate_alpha( self ):
                self.alpha = 1.0 - ( self.K / self.K_s );

        def _calculate_K_p( self ):
                self.K_p = self.phi * self.K / self.alpha;

        def _calculate_B( self ):
                self.B = self.R / self.H;

        def _calculate_K_u( self ):
                self.K_u = self.K / ( 1.0 - self.alpha * self.B );

        def _calculate_ni( self ):
                self.ni = ( 3.0 * self.K - 2.0 * self.G ) / ( 2.0 * ( 3.0 * self.K + self.G ) );

        def _calculate_ni_u( self ):
                self.ni_u = ( ( 3.0 * self.ni + self.alpha * self.B * ( 1.0 - 2.0 * self.ni ) ) /
                              ( 3.0 - self.alpha * self.B * ( 1.0 - 2.0 * self.ni ) ) );

        def _calculate_K_ni_u( self ):
                self.K_ni_u = ( 3.0 * self.K_u * ( 1.0 - self.ni_u ) ) / ( 1.0 + self.ni_u );

        def _calculate_c_s( self ):
                self.c_s = 1.0 / self.K_s;

        def _calculate_c_f( self ):
                self.c_f = 1.0 / self.K_f;

        def _calculate_gama( self ):
                self.gama = ( self.B * ( 1.0 + self.ni_u ) ) / ( 3.0 * ( 1.0 - self.ni_u ) );

        def _calculate_c( self ):
                self.c = ( ( 2.0 * self.permeability * self.G * ( 1.0 - self.ni ) * ( self.ni_u - self.ni ) ) /
                           ( self.mi * ( self.alpha ** 2.0 ) * ( 1.0 - self.ni_u ) * ( ( 1.0 - 2.0 * self.ni ) ** 2.0 ) ) );


        def _calculateFunctionToFindTheRoots( self, x ):
                y = math.tan( x ) - ( ( 1 - self.ni ) / ( self.ni_u - self.ni ) ) * x;
                return y;


        def _calculateRoots( self, numberOfRoots, maxIterations = 100, maxResidue = 1.0e-12 ):
                roots = [ ];

                for i in range( 0, numberOfRoots ):
                        x_A = i * math.pi + maxResidue;
                        x_B = i * math.pi + ( math.pi / 2 ) - maxResidue;
                        x_C = ( x_A + x_B ) / 2;
                        y_C = self._calculateFunctionToFindTheRoots( x_C );

                        iteration = 0;
                        residue = 1.0;

                        while iteration < maxIterations and residue > maxResidue and y_C != 0:
                                y_A = self._calculateFunctionToFindTheRoots( x_A );
                                y_C = self._calculateFunctionToFindTheRoots( x_C );

                                if y_A * y_C > 0.0:
                                        x_A = x_C;
                                else:
                                        x_B = x_C;

                                x_C = ( x_A + x_B ) / 2;
                                
                                residue = x_B - x_A;
                                iteration += 1;

                        roots.append( x_C );

                return roots;


##        def _calculatePressure( self, xPosition, time, numberOfSummationTerms = 400 ):
##                roots = self._calculateRoots( numberOfSummationTerms );
##                summationResult = 0.0;
##
##                for i in range( 0, numberOfSummationTerms ):
##                        term_1 = math.sin( roots[ i ] ) / ( roots[ i ] - math.sin( roots[ i ] ) * math.cos( roots[ i ] ) );
##                        term_2 = math.cos( roots[ i ] * xPosition / self.lenght ) - math.cos( roots[ i ] );
##                        term_3 = math.exp( - ( ( self.c * time * ( roots[ i ] ** 2 ) ) / ( self.lenght ** 2 ) ) );
##                        summationResult += term_1 * term_2 * term_3;
##
##                pressureValue = ( ( 2 * self.F * self.B * ( 1 + self.ni_u ) ) / ( 3 * self.lenght ) ) * summationResult;
##
##                return pressureValue;
                        

##        def _calculateVertStress( self, xPosition, time, numberOfSummationTerms = 400 ):
##                roots = self._calculateRoots( numberOfSummationTerms );
##                summationResult_1 = 0.0;
##                summationResult_2 = 0.0;
##
##                for i in range( 0, numberOfSummationTerms ):
##                        term_1 = math.sin( roots[ i ] ) / ( roots[ i ] - math.sin( roots[ i ] ) * math.cos( roots[ i ] ) );
##                        term_2 = math.cos( roots[ i ] * xPosition / self.lenght );
##                        term_3 = math.exp( - ( ( self.c * time * ( roots[ i ] ** 2 ) ) / ( self.lenght ** 2 ) ) );
##                        summationResult_1 += term_1 * term_2 * term_3;
##
##                for i in range( 0, numberOfSummationTerms ):
##                        term_1 = ( math.sin( roots[ i ] ) * math.cos( roots[ i ] ) ) / ( roots[ i ] - math.sin( roots[ i ] ) * math.cos( roots[ i ] ) );
##                        term_2 = math.exp( - ( ( self.c * time * ( roots[ i ] ** 2 ) ) / ( self.lenght ** 2 ) ) );
##                        summationResult_2 += term_1 * term_2;
##
##                vertStressValue = ( - ( 2 * self.F * ( self.ni_u - self.ni ) ) / ( self.lenght * ( 1 - self.ni ) ) * summationResult_1 -
##                                  self.F / self.lenght +
##                                  2 * self.F / self.lenght * summationResult_2 );
##
##                return vertStressValue;


##        def _calculateHorDisplacement( self, xPosition, time, numberOfSummationTerms = 400 ):
##                roots = self._calculateRoots( numberOfSummationTerms );
##                summationResult_1 = 0.0;
##                summationResult_2 = 0.0;
##
##                for i in range( 0, numberOfSummationTerms ):
##                        term_1 = ( math.sin( roots[ i ] ) * math.cos( roots[ i ] ) ) / ( roots[ i ] - math.sin( roots[ i ] ) * math.cos( roots[ i ] ) );
##                        term_2 = math.exp( - ( ( self.c * time * ( roots[ i ] ** 2 ) ) / ( self.lenght ** 2 ) ) );
##                        summationResult_1 += term_1 * term_2;
##
##                for i in range( 0, numberOfSummationTerms ):
##                        term_1 = math.cos( roots[ i ] ) / ( roots[ i ] - math.sin( roots[ i ] ) * math.cos( roots[ i ] ) );
##                        term_2 = math.sin( roots[ i ] * xPosition / self.lenght );
##                        term_3 = math.exp( - ( ( self.c * time * ( roots[ i ] ** 2 ) ) / ( self.lenght ** 2 ) ) );
##                        summationResult_2 += term_1 * term_2 * term_3;
##
##                firstTerm = ( ( self.F * self.ni ) / ( 2 * self.G * self.lenght ) - ( self.F * self.ni_u ) / ( self.G * self.lenght ) * summationResult_1 ) * xPosition;
##                secondTerm = self.F / self.G * summationResult_2;
##
##                horDisplacementValue = firstTerm + secondTerm;
##
##                return horDisplacementValue;


##        def _calculateVertDisplacement( self, yPosition, time, numberOfSummationTerms = 400 ):
##                roots = self._calculateRoots( numberOfSummationTerms );
##                summationResult = 0.0;
##
##                for i in range( 0, numberOfSummationTerms ):
##                        term_1 = ( math.sin( roots[ i ] ) * math.cos( roots[ i ] ) ) / ( roots[ i ] - math.sin( roots[ i ] ) * math.cos( roots[ i ] ) );
##                        term_2 = math.exp( - ( ( self.c * time * ( roots[ i ] ** 2 ) ) / ( self.lenght ** 2 ) ) );
##                        summationResult += term_1 * term_2;
##
##                vertDisplacementValue = ( ( self.F * ( 1.0 - self.ni_u ) ) / ( self.G * self.lenght ) * summationResult -
##                                          ( self.F * ( 1.0 - self.ni ) ) / ( 2.0 * self.G * self.lenght ) ) * yPosition;
##
##                return vertDisplacementValue;


        # Class interface -----------------------------------------------------------------------
        def getXPositionValues( self, nx = 200 ):
                dx = self.lenght / ( nx - 1.0 );
                positionValues = [ ];

                for i in range( 0, nx ):
                        positionValues.append( i * dx );
                
                return positionValues;


        def getXPositionValuesNormalized( self, nx = 200 ):
                positionValues = self.getXPositionValues( nx );
                positionValuesNormalized = [ ];

                for i in range( 0, len( positionValues ) ):
                        positionValuesNormalized.append( positionValues[ i ] / self.lenght );

                return positionValuesNormalized;


        def getYPositionValues( self, ny = 200 ):
                dy = self.height / ( ny - 1 );
                positionValues = [ ];

                for i in range( 0, ny ):
                        positionValues.append( i * dy );

                return positionValues;


        def getYPositionValuesNormalized( self, ny = 200 ):
                positionValues = self.getYPositionValues( ny );
                positionValuesNormalized = [ ];

                for i in range( 0, len( positionValues ) ):
                        positionValuesNormalized.append( positionValues[ i ] / self.height );

                return positionValuesNormalized;


        def getPressureValue( self, xPosition, time, numberOfSummationTerms = 200, roots = [ ] ):
                if time == 0.0:
                        pressureValue = self.F * self.B * ( 1 + self.ni_u ) / ( self.lenght * 3 )

                        return pressureValue

                else:
                        if len( roots ) == 0:
                                roots = self._calculateRoots( numberOfSummationTerms )

                        summationResult = 0.0

                        for i in range( 0, numberOfSummationTerms ):
                                term_1 = math.sin( roots[ i ] ) / ( roots[ i ] - math.sin( roots[ i ] ) * math.cos( roots[ i ] ) )
                                term_2 = math.cos( roots[ i ] * xPosition / self.lenght ) - math.cos( roots[ i ] )
                                term_3 = math.exp( - ( ( self.c * time * ( roots[ i ] ** 2 ) ) / ( self.lenght ** 2 ) ) )
                                summationResult += term_1 * term_2 * term_3

                        pressureValue = ( ( 2 * self.F * self.B * ( 1 + self.ni_u ) ) / ( 3 * self.lenght ) ) * summationResult

                        return pressureValue


        def getVertStressValue( self, xPosition, time, numberOfSummationTerms = 200, roots = [ ] ):
                if time == 0.0:
                        vertStressValue = - self.F / self.lenght

                        return vertStressValue

                else:                
                        if len( roots ) == 0:
                                roots = self._calculateRoots( numberOfSummationTerms )
                        
                        summationResult_1 = 0.0
                        summationResult_2 = 0.0

                        for i in range( 0, numberOfSummationTerms ):
                                term_1 = math.sin( roots[ i ] ) / ( roots[ i ] - math.sin( roots[ i ] ) * math.cos( roots[ i ] ) )
                                term_2 = math.cos( roots[ i ] * xPosition / self.lenght )
                                term_3 = math.exp( - ( ( self.c * time * ( roots[ i ] ** 2 ) ) / ( self.lenght ** 2 ) ) )
                                summationResult_1 += term_1 * term_2 * term_3

                        for i in range( 0, numberOfSummationTerms ):
                                term_1 = ( math.sin( roots[ i ] ) * math.cos( roots[ i ] ) ) / ( roots[ i ] - math.sin( roots[ i ] ) * math.cos( roots[ i ] ) )
                                term_2 = math.exp( - ( ( self.c * time * ( roots[ i ] ** 2 ) ) / ( self.lenght ** 2 ) ) )
                                summationResult_2 += term_1 * term_2

                        vertStressValue = ( - ( 2 * self.F * ( self.ni_u - self.ni ) ) / ( self.lenght * ( 1 - self.ni ) ) * summationResult_1 -
                                          self.F / self.lenght +
                                          2 * self.F / self.lenght * summationResult_2 )

                        return vertStressValue


        def getHorDisplacementValue( self, xPosition, time, numberOfSummationTerms = 200, roots = [ ] ):

                if len( roots ) == 0:
                        roots = self._calculateRoots( numberOfSummationTerms );

                summationResult_1 = 0.0;
                summationResult_2 = 0.0;

                for i in range( 0, numberOfSummationTerms ):
                        term_1 = ( math.sin( roots[ i ] ) * math.cos( roots[ i ] ) ) / ( roots[ i ] - math.sin( roots[ i ] ) * math.cos( roots[ i ] ) );
                        term_2 = math.exp( - ( ( self.c * time * ( roots[ i ] ** 2 ) ) / ( self.lenght ** 2 ) ) );
                        summationResult_1 += term_1 * term_2;

                for i in range( 0, numberOfSummationTerms ):
                        term_1 = math.cos( roots[ i ] ) / ( roots[ i ] - math.sin( roots[ i ] ) * math.cos( roots[ i ] ) );
                        term_2 = math.sin( roots[ i ] * xPosition / self.lenght );
                        term_3 = math.exp( - ( ( self.c * time * ( roots[ i ] ** 2 ) ) / ( self.lenght ** 2 ) ) );
                        summationResult_2 += term_1 * term_2 * term_3;

                firstTerm = ( ( self.F * self.ni ) / ( 2 * self.G * self.lenght ) - ( self.F * self.ni_u ) / ( self.G * self.lenght ) * summationResult_1 ) * xPosition;
                secondTerm = self.F / self.G * summationResult_2;

                horDisplacementValue = firstTerm + secondTerm;

                return horDisplacementValue;


        def getVertDisplacementValue( self, yPosition, time, numberOfSummationTerms = 200, roots = [ ] ):

                if len( roots ) == 0:
                        roots = self._calculateRoots( numberOfSummationTerms );

                summationResult = 0.0;

                for i in range( 0, numberOfSummationTerms ):
                        term_1 = ( math.sin( roots[ i ] ) * math.cos( roots[ i ] ) ) / ( roots[ i ] - math.sin( roots[ i ] ) * math.cos( roots[ i ] ) );
                        term_2 = math.exp( - ( ( self.c * time * ( roots[ i ] ** 2 ) ) / ( self.lenght ** 2 ) ) );
                        summationResult += term_1 * term_2;

                vertDisplacementValue = ( ( self.F * ( 1.0 - self.ni_u ) ) / ( self.G * self.lenght ) * summationResult -
                                          ( self.F * ( 1.0 - self.ni ) ) / ( 2.0 * self.G * self.lenght ) ) * yPosition;

                return vertDisplacementValue;


        def getPressureValuesConstTime( self, time, numberOfSummationTerms = 200, nx = 200 ):
                positionValues = self.getXPositionValues( nx );
                roots = self._calculateRoots( numberOfSummationTerms );
                pressureValues = [ ];

                for i in range( 0, len( positionValues ) ):
                        pressureValue = self.getPressureValue( positionValues[ i ], time, numberOfSummationTerms, roots );
                        pressureValues.append( pressureValue );

                return pressureValues;


        def getPressureValuesNormalizedConstTime( self, time, numberOfSummationTerms = 200, nx = 200 ):
                initialPressure = self.getPressureValue( 0.0, 0.0, numberOfSummationTerms );
                pressureValues = self.getPressureValuesConstTime( time, numberOfSummationTerms, nx );
                pressureValuesNormalized = [ ];

                for i in range( 0, len( pressureValues ) ):
                        pressureValuesNormalized.append( pressureValues[ i ] / initialPressure );

                return pressureValuesNormalized;


        def getVertStressValuesConstTime( self, time, numberOfSummationTerms = 200, nx = 200 ):
                positionValues = self.getXPositionValues( nx );
                roots = self._calculateRoots( numberOfSummationTerms );
                vertStressValues = [ ];

                for i in range( 0, len( positionValues ) ):
                        vertStressValue = self.getVertStressValue( positionValues[ i ], time, numberOfSummationTerms, roots );
                        vertStressValues.append( vertStressValue );

                return vertStressValues;


        def getVertStressValuesNormalizedConstTime( self, time, numberOfSummationTerms = 200, nx = 200 ):
                initialVertStress = self.getVertStressValue( 0.0, 0.0, numberOfSummationTerms )
                vertStressValues = self.getVertStressValuesConstTime( time, numberOfSummationTerms, nx )
                vertStressValuesNormalized = []

                for i in range( 0, len( vertStressValues ) ):
                        vertStressValuesNormalized.append( vertStressValues[ i ] / initialVertStress )

                return vertStressValuesNormalized


        def getHorDisplacementValuesConstTime( self, time, numberOfSummationTerms = 200, nx = 200 ):
                positionValues = self.getXPositionValues( nx );
                roots = self._calculateRoots( numberOfSummationTerms );
                horDisplacementValues = [ ];

                for i in range( 0, len( positionValues ) ):
                        horDisplacementValue = self.getHorDisplacementValue( positionValues[ i ], time, numberOfSummationTerms, roots );
                        horDisplacementValues.append( horDisplacementValue );

                return horDisplacementValues;


        def getVertDisplacementValuesConstTime( self, time, numberOfSummationTerms = 200, ny = 200 ):
                positionValues = self.getYPositionValues( ny );
                roots = self._calculateRoots( numberOfSummationTerms );
                vertDisplacementValues = [ ];

                for i in range( 0, len( positionValues ) ):
                        vertDisplacementValue = self.getVertDisplacementValue( positionValues[ i ], time, numberOfSummationTerms, roots );
                        vertDisplacementValues.append( vertDisplacementValue );

                return vertDisplacementValues;


        def getTimeValues( self, totalTimeInterval, timePoints = 200 ):
                dt = totalTimeInterval / ( timePoints - 1 );
                timeValues = [ ];

                for i in range( 0, timePoints ):
                        timeValues.append( i * dt );

                return timeValues;                


        def getPressureValuesConstPosition( self, xPosition, totalTimeInterval, numberOfSummationTerms = 200, timePoints = 200 ):
                timeValues = self.getTimeValues( totalTimeInterval, timePoints );
                roots = self._calculateRoots( numberOfSummationTerms );
                pressureValues = [ ];

                for i in range( 0, len( timeValues ) ):
                        pressureValue = self.getPressureValue( xPosition, timeValues[ i ], numberOfSummationTerms, roots );
                        pressureValues.append( pressureValue );

                return pressureValues;


        def getPressureValuesNormalizedConstPosition( self, xPosition, totalTimeInterval, numberOfSummationTerms = 200, timePoints = 200 ):
                initialPressure = self.getPressureValue( 0.0, 0.0, numberOfSummationTerms );
                pressureValues = self.getPressureValuesConstPosition( xPosition, totalTimeInterval, numberOfSummationTerms, timePoints );
                pressureValuesNormalized = [ ];

                for i in range( 0, len( pressureValues ) ):
                        pressureValuesNormalized.append( pressureValues[ i ] / initialPressure );

                return pressureValuesNormalized;

        
        def getVertStressValuesConstPosition( self, xPosition, totalTimeInterval, numberOfSummationTerms = 200, timePoints = 200 ):
                timeValues = self.getTimeValues( totalTimeInterval, timePoints );
                roots = self._calculateRoots( numberOfSummationTerms );
                vertStressValues = [ ];

                for i in range( 0, len( timeValues ) ):
                        vertStressValue = self.getVertStressValue( xPosition, timeValues[ i ], numberOfSummationTerms, roots );
                        vertStressValues.append( vertStressValue );

                return vertStressValues;


        def getHorDisplacementValuesConstPosition( self, xPosition, totalTimeInterval, numberOfSummationTerms = 200, timePoints = 200 ):
                timeValues = self.getTimeValues( totalTimeInterval, timePoints );
                roots = self._calculateRoots( numberOfSummationTerms );
                horDisplacementValues = [ ];

                for i in range( 0, len( timeValues ) ):
                        horDisplacementValue = self.getHorDisplacementValue( xPosition, timeValues[ i ], numberOfSummationTerms, roots );
                        horDisplacementValues.append( horDisplacementValue );

                return horDisplacementValues;


        def getVertDisplacementValuesConstPosition( self, yPosition, totalTimeInterval, numberOfSummationTerms = 200, timePoints = 200 ):
                timeValues = self.getTimeValues( totalTimeInterval, timePoints );
                roots = self._calculateRoots( numberOfSummationTerms );
                vertDisplacementValues = [ ];

                for i in range( 0, len( timeValues ) ):
                        vertDisplacementValue = self.getVertDisplacementValue( yPosition, timeValues[ i ], numberOfSummationTerms, roots );
                        vertDisplacementValues.append( vertDisplacementValue );

                return vertDisplacementValues;        
        

# EXAMPLE =======================================================================================

import matplotlib.pyplot as plt

if __name__ == '__main__':
        lenght = 5.0
        height = 1.0
        F = 5.0e+7
        permeability = 1.0e-15
        phi = 0.19
        mi = 0.001
        K = 8.0e+9
        K_s = 3.6e+10
        K_f = 3.3e+9
        G = 6.0e+9
        K_phi = 3.6e+10
        
        example = MandelsProblemAnalytical( lenght, height, F, permeability, phi, mi, K, K_s, K_f, G, K_phi )
        AxisX = example.getXPositionValues();
        AxisY = example.getYPositionValues();
        AxisXNormalized = example.getXPositionValuesNormalized();
        AxisYNormalized = example.getYPositionValuesNormalized();


##        plt.figure();
##
##        PressureConstTime10 = example.getPressureValuesConstTime( 10.0 );
##        PressureConstTime100 = example.getPressureValuesConstTime( 100.0 );
##        PressureConstTime1000 = example.getPressureValuesConstTime( 1000.0 );
##        PressureConstTime3000 = example.getPressureValuesConstTime( 3000.0 );
##
##        plt.plot( AxisX, PressureConstTime10, 'blue' );
##        plt.plot( AxisX, PressureConstTime100, 'red' );
##        plt.plot( AxisX, PressureConstTime1000, 'green' );
##        plt.plot( AxisX, PressureConstTime3000, 'black' );
##
##        plt.grid( True );
##        plt.xlabel( 'x [m]' );
##        plt.ylabel( 'Pressure [Pa]' );
##        plt.axis( [ 0, 10, 0, 3.2e+6 ] );


##        plt.figure();
##        
##        PressureConstTimeNormalized10 = example.getPressureValuesNormalizedConstTime( 10.0 );
##        PressureConstTimeNormalized100 = example.getPressureValuesNormalizedConstTime( 100.0 );
##        PressureConstTimeNormalized1000 = example.getPressureValuesNormalizedConstTime( 1000.0 );
##        PressureConstTimeNormalized3000 = example.getPressureValuesNormalizedConstTime( 3000.0 );
##
##        plt.plot( AxisXNormalized, PressureConstTimeNormalized10, 'blue' );
##        plt.plot( AxisXNormalized, PressureConstTimeNormalized100, 'red' );
##        plt.plot( AxisXNormalized, PressureConstTimeNormalized1000, 'green' );
##        plt.plot( AxisXNormalized, PressureConstTimeNormalized3000, 'black' );
##
##        plt.grid( True );
##        plt.xlabel( 'x/L' );
##        plt.ylabel( 'p/p_0' );
##        plt.axis( [ 0, 1, 0, 1.1 ] );


##        plt.figure();
##
##        VertStressConstTime10 = example.getVertStressValuesConstTime( 10.0 );
##        VertStressConstTime100 = example.getVertStressValuesConstTime( 100.0 );
##        VertStressConstTime1000 = example.getVertStressValuesConstTime( 1000.0 );
##        VertStressConstTime3000 = example.getVertStressValuesConstTime( 3000.0 );
##
##        plt.plot( AxisX, VertStressConstTime10, 'blue' );
##        plt.plot( AxisX, VertStressConstTime100, 'red' );
##        plt.plot( AxisX, VertStressConstTime1000, 'green' );
##        plt.plot( AxisX, VertStressConstTime3000, 'black' );
##
##        plt.grid( True );
##        plt.xlabel( 'x [m]' );
##        plt.ylabel( 'Vertical normal stress [Pa]' );


##        plt.figure();
##
##        HorDisplacementConstTime0 = example.getHorDisplacementValuesConstTime( 0.0 );
##        HorDisplacementConstTime200 = example.getHorDisplacementValuesConstTime( 200.0 );
##        HorDisplacementConstTime1000 = example.getHorDisplacementValuesConstTime( 1000.0 );
##        HorDisplacementConstTime10000 = example.getHorDisplacementValuesConstTime( 10000.0 );
##
##        plt.plot( AxisX, HorDisplacementConstTime0, 'blue', label = '0' );
##        plt.plot( AxisX, HorDisplacementConstTime200, 'red', label = '200' );
##        plt.plot( AxisX, HorDisplacementConstTime1000, 'green', label = '1000' );
##        plt.plot( AxisX, HorDisplacementConstTime10000, 'black', label = '10000' );
##
##        plt.grid( True );
##        plt.xlabel( 'x [m]' );
##        plt.ylabel( 'Horizontal displacement [m]' );
##        plt.legend( title = 'Time [s]', fontsize = 12, loc = 'best' );


##        plt.figure();
##
##        VertDisplacementConstTime0 = example.getVertDisplacementValuesConstTime( 0.0 );
##        VertDisplacementConstTime200 = example.getVertDisplacementValuesConstTime( 200.0 );
##        VertDisplacementConstTime1000 = example.getVertDisplacementValuesConstTime( 1000.0 );
##        VertDisplacementConstTime10000 = example.getVertDisplacementValuesConstTime( 10000.0 );
##
##        plt.plot( VertDisplacementConstTime0, AxisY, 'blue', label = '0' );
##        plt.plot( VertDisplacementConstTime200, AxisY, 'red', label = '200' );
##        plt.plot( VertDisplacementConstTime1000, AxisY, 'green', label = '1000' );
##        plt.plot( VertDisplacementConstTime10000, AxisY, 'black', label = '10000' );
##
##        plt.grid( True );
##        plt.xlabel( 'Vertical displacement [m]' );
##        plt.ylabel( 'y [m]' );
##        plt.legend( title = 'Time [s]', fontsize = 12 );


        totalTimeInterval = 1.0e+5;
        timeValues = example.getTimeValues( totalTimeInterval );


##        plt.figure();
##
##        PressureConstPosition0 = example.getPressureValuesConstPosition( 0.0, totalTimeInterval );
##
##        plt.plot( timeValues, PressureConstPosition0, 'black' );
##
##        plt.grid( True );
##        plt.xlabel( 'Time [s]' );
##        plt.ylabel( 'Pressure [Pa]' );


##        plt.figure();
##
##        PressureConstPositionNormalized0 = example.getPressureValuesNormalizedConstPosition( 0.0, totalTimeInterval );
##
##        plt.plot( timeValues, PressureConstPositionNormalized0, 'black' );
##
##        plt.grid( True );
##        plt.xlabel( 'Time [s]' );
##        plt.ylabel( 'p/p_0' );


##        plt.figure();
##
##        VertStressConstPosition0 = example.getVertStressValuesConstPosition( 0.0, totalTimeInterval );
##        VertStressConstPositionLenght = example.getVertStressValuesConstPosition( example.lenght, totalTimeInterval );
##
##        plt.plot( timeValues, VertStressConstPosition0, 'black', label = '0' );
##        plt.plot( timeValues, VertStressConstPositionLenght, 'red', label = 'Lenght' );
##
##        plt.grid( True );
##        plt.xlabel( 'Time [s]' );
##        plt.ylabel( 'Vertical normal stress [Pa]' );
##        plt.legend( title = 'Position', fontsize = 12 );


##        plt.figure();
##
##        HorDisplacementConstPositionLenght = example.getHorDisplacementValuesConstPosition( example.lenght, totalTimeInterval );
##        HorDisplacementConstPositionHalfLenght = example.getHorDisplacementValuesConstPosition( example.lenght / 2, totalTimeInterval );
##
##        plt.plot( timeValues, HorDisplacementConstPositionLenght, 'black', label = 'Lenght' );
##        plt.plot( timeValues, HorDisplacementConstPositionHalfLenght, 'red', label = 'Lenght/2' );
##
##        plt.grid( True );
##        plt.xlabel( 'Time [s]' );
##        plt.ylabel( 'Horizontal displacement (u) [m]' );
##        plt.legend( title = 'Position', fontsize = 12 );


##        plt.figure();
##
##        VertDisplacementConstPositionHeight = example.getVertDisplacementValuesConstPosition( example.height, totalTimeInterval );
##
##        plt.plot( timeValues, VertDisplacementConstPositionHeight, 'black', label = 'Height' );
##
##        plt.grid( True );
##        plt.xlabel( 'Time [s]' );
##        plt.ylabel( 'Vertical displacement (v) [m]' );
##        plt.legend( title = 'Position', fontsize = 12 );


        plt.show();
