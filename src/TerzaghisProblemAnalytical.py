# ABREVIATIONS USED =============================================================================

# ny - Number of points in the y direction
# height - Domain height
# tao_0 - Normal stress
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
# c_m - Geertma's uniaxial poroelastic expansion coefficient
# p_0 - Inicial pore pressure


import math;


# CLASS DEFINITION ==============================================================================

class TerzaghisProblemAnalytical( object ):

        # Constructor ---------------------------------------------------------------------------
        def __init__( self, height, tao_0, permeability, phi, mi, K, K_s, K_f, G, K_phi ):
                self.height = height;
                self.tao_0 = tao_0;
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
                self._calculate_c_m();
                self._calculate_p_0();
                

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

        def _calculate_c_m( self ):
                self.c_m = ( self.alpha * ( 1.0 + self.ni ) ) / ( 3.0 * self.K * ( 1.0 - self.ni ) );

        def _calculate_p_0( self ):
                self.p_0 = self.gama * self.tao_0;


        # Class interface -----------------------------------------------------------------------
        def getPositionValues( self, ny = 200 ):
                dy = self.height / ( ny - 1.0 );
                positionValues = [ ];

                for i in range( 0, ny ):
                        positionValues.append( i * dy );
                
                return positionValues;


        def getPositionValuesNormalized( self, ny = 200 ):
                positionValues = self.getPositionValues( ny );
                positionValuesNormalized = [ ];

                for i in range( 0, len( positionValues ) ):
                        positionValuesNormalized.append( positionValues[ i ] / self.height );

                return positionValuesNormalized;


        def getPressureValue( self, yPosition, time, numberOfSummationTerms = 200 ):
                position = self.height - yPosition;
                
                if time == 0.0:
                        pressureValue = self.p_0
                        
                        return pressureValue
                
                else:
                        summationResult = 0
                        
                        for j in range( 0, numberOfSummationTerms ):
                                term_1 = 1.0 / ( 2.0 * j + 1.0 )
                                term_2 = ( math.exp( - ( ( time * self.c * ( math.pi ** 2.0 ) * ( ( 2.0 * j + 1.0 ) ** 2.0 ) ) /
                                                        ( 4.0 * ( self.height ** 2.0 ) ) ) ) )
                                term_3 = math.sin( ( math.pi * position * ( 2.0 * j + 1 ) ) / ( 2.0 * self.height ) )
                                summationResult += term_1 * term_2 * term_3

                        pressureValue = 4.0 * self.gama * self.tao_0 * summationResult / math.pi
                        
                        return pressureValue


        def getDisplacementValue( self, yPosition, time, numberOfSummationTerms = 200 ):
                position = self.height - yPosition;

                if time == 0.0:
                        displacementValue = - ( self.tao_0 * ( self.height - position ) * ( 1 + self.ni_u ) / ( 3 * self.K_u * ( 1 - self.ni_u ) ) )

                        return displacementValue

                else:                
                        summationResult = 0;
                        initialDisplacementValue = ( ( self.tao_0 * ( 1.0 - 2.0 * self.ni_u ) * ( self.height - position ) ) /
                                                     ( 2.0 * self.G * ( 1.0 - self.ni_u ) ) )
                        
                        for j in range( 0, numberOfSummationTerms ):
                                term_1 = 1.0 / ( ( 2.0 * j + 1.0 ) ** 2 )
                                term_2 = ( math.exp( - ( ( self.c * time * ( math.pi ** 2.0 ) * ( ( 2.0 * j + 1.0 ) ** 2.0 ) ) /
                                                         ( 4.0 * ( self.height ** 2.0 ) ) ) ) )
                                term_3 = math.cos( ( math.pi * position * ( 2.0 * j + 1.0 ) ) / ( 2 * self.height ) )
                                summationResult += term_1 * term_2 * term_3

                        displacementValue = - ( initialDisplacementValue + self.c_m * self.gama * self.tao_0 *
                                              ( ( self.height - position ) - ( 8.0 * self.height / ( math.pi ** 2.0 ) ) * summationResult ) )

                        return displacementValue


##        def getPressureValuesConstTime( self, time, numberOfSummationTerms = 200, ny = 200 ):
##                positionValues = self.getPositionValues( ny );
##                pressureValues = [ ];
##                
##                for i in range( 0, len( positionValues ) ):
##                        position = self.height - positionValues[ i ];
##                        summationResult = 0;
##                        
##                        for j in range( 0, numberOfSummationTerms ):
##                                term_1 = 1.0 / ( 2.0 * j + 1.0 );
##                                term_2 = ( math.exp( - ( ( time * self.c * ( math.pi ** 2.0 ) * ( ( 2.0 * j + 1.0 ) ** 2.0 ) ) /
##                                                         ( 4.0 * ( self.height ** 2.0 ) ) ) ) );
##                                term_3 = math.sin( ( math.pi * position * ( 2.0 * j + 1 ) ) / ( 2.0 * self.height ) );
##                                summationResult += term_1 * term_2 * term_3;
##                                
##                        pressureValue = 4.0 * self.gama * self.tao_0 * summationResult / math.pi;
##                        pressureValues.append( pressureValue );
##                        
##                return pressureValues;


        def getPressureValuesConstTime( self, time, numberOfSummationTerms = 200, ny = 200 ):
                positionValues = self.getPositionValues( ny );
                pressureValues = [ ];

                for i in range( 0, len( positionValues ) ):
                        pressureValue = self.getPressureValue( positionValues[ i ], time, numberOfSummationTerms );
                        pressureValues.append( pressureValue );

                return pressureValues;


        def getPressureValuesNormalizedConstTime( self, time, numberOfSummationTerms = 200, ny = 200 ): # p / p_0
                pressureValues = self.getPressureValuesConstTime( time, numberOfSummationTerms, ny );
                pressureValuesNormalized = [ ];

                for i in range( 0, len( pressureValues ) ):
                        pressureValuesNormalized.append( pressureValues[ i ] / self.p_0 );
                        
                return pressureValuesNormalized;


##        def getDisplacementValuesConstTime( self, time, numberOfSummationTerms = 200, ny = 200 ):
##                positionValues = self.getPositionValues( ny );
##                displacementValues = [ ];
##
##                for i in range( 0, len( positionValues ) ):
##                        position = self.height - positionValues[ i ];
##                        initialDisplacementValue = ( ( self.tao_0 * ( 1.0 - 2.0 * self.ni_u ) * ( self.height - position ) ) /
##                                                     ( 2.0 * self.G * ( 1.0 - self.ni_u ) ) );
##                        summationResult = 0;
##
##                        for j in range( 0, numberOfSummationTerms ):
##                                term_1 = 1.0 / ( ( 2.0 * j + 1.0 ) ** 2 );
##                                term_2 = ( math.exp( - ( ( self.c * time * ( math.pi ** 2.0 ) * ( ( 2.0 * j + 1.0 ) ** 2.0 ) ) /
##                                                         ( 4.0 * ( self.height ** 2.0 ) ) ) ) );
##                                term_3 = math.cos( ( math.pi * position * ( 2.0 * j + 1.0 ) ) / ( 2 * self.height ) );
##                                summationResult += term_1 * term_2 * term_3;
##
##                        displacementValue = - ( initialDisplacementValue + self.c_m * self.gama * self.tao_0 *
##                                              ( ( self.height - position ) - ( 8.0 * self.height / ( math.pi ** 2.0 ) ) * summationResult ) );
##                        displacementValues.append( displacementValue );
##
##                return displacementValues;


        def getDisplacementValuesConstTime( self, time, numberOfSummationTerms = 200, ny = 200 ):
                positionValues = self.getPositionValues( ny );
                displacementValues = [ ];

                for i in range( 0, len( positionValues ) ):
                        displacementValue = self.getDisplacementValue( positionValues[ i ], time, numberOfSummationTerms );
                        displacementValues.append( displacementValue );

                return displacementValues;


        def getDisplacementValuesNormalizedConstTime( self, time, numberOfSummationTerms = 200, ny = 200 ): # ( v - v_inicial ) / ( v_final - v_inicial )
                positionValues = self.getPositionValues( ny );
                displacementValues = self.getDisplacementValuesConstTime( time, numberOfSummationTerms, ny );
                displacementValuesNormalized = [ ];

                for i in range( 0, len( displacementValues ) ):
                        position = self.height - positionValues[ i ];
                        initialDisplacementValue = ( ( self.tao_0 * ( 1.0 - 2.0 * self.ni_u ) * ( self.height - position ) ) /
                                                     ( 2.0 * self.G * ( 1.0 - self.ni_u ) ) );
                        finalDisplacementValue = initialDisplacementValue + self.c_m * self.gama * self.tao_0 * ( self.height - position );

                        if i == 0:
                                displacementValueNormalized = 0;
                        else:
                                displacementValueNormalized = ( ( - displacementValues[ i ] - initialDisplacementValue ) /
                                                                ( finalDisplacementValue - initialDisplacementValue ) );

                        displacementValuesNormalized.append( displacementValueNormalized );

                displacementValuesNormalized[ 0 ] = displacementValuesNormalized[ 1 ];
                
                return displacementValuesNormalized;


        def getTimeValues( self, totalTimeInterval, timePoints = 200 ):
                dt = totalTimeInterval / ( timePoints - 1 );
                timeValues = [ ];

                for i in range( 0, timePoints ):
                        timeValues.append( i * dt );

                return timeValues;                


##        def getPressureValuesConstPosition( self, position, totalTimeInterval, numberOfSummationTerms = 200, timePoints = 200 ):
##                timeValues = self.getTimeValues( totalTimeInterval, timePoints );
##                position = self.height - position;
##                pressureValues = [ ];
##
##                for i in range( 0, len( timeValues ) ):
##                        summationResult = 0;
##
##                        for j in range( 0, numberOfSummationTerms ):
##                                term_1 = 1.0 / ( 2.0 * j + 1.0 );
##                                term_2 = ( math.exp( - ( ( timeValues[ i ] * self.c * ( math.pi ** 2.0 ) * ( ( 2.0 * j + 1.0 ) ** 2.0 ) ) /
##                                                         ( 4.0 * ( self.height ** 2.0 ) ) ) ) );
##                                term_3 = math.sin( ( math.pi * position * ( 2.0 * j + 1 ) ) / ( 2.0 * self.height ) );
##                                summationResult += term_1 * term_2 * term_3;
##
##                        pressureValue = 4.0 * self.gama * self.tao_0 * summationResult / math.pi;
##                        pressureValues.append( pressureValue );
##
##                return pressureValues;


        def getPressureValuesConstPosition( self, position, totalTimeInterval, numberOfSummationTerms = 200, timePoints = 200 ):
                timeValues = self.getTimeValues( totalTimeInterval, timePoints );
                pressureValues = [ ];

                for i in range( 0, len( timeValues ) ):
                        pressureValue = self.getPressureValue( position, timeValues[ i ], numberOfSummationTerms );
                        pressureValues.append( pressureValue );

                return pressureValues;


        def getPressureValuesNormalizedConstPosition( self, position, totalTimeInterval, numberOfSummationTerms = 200, timePoints = 200 ): # p / p_0
                pressureValues = self.getPressureValuesConstPosition( position, totalTimeInterval, numberOfSummationTerms, timePoints );
                pressureValuesNormalized = [ ];

                for i in range( 0, len( pressureValues ) ):
                        pressureValuesNormalized.append( pressureValues[ i ] / self.p_0 );

                return pressureValuesNormalized;


##        def getDisplacementValuesConstPosition( self, position, totalTimeInterval, numberOfSummationTerms = 200, timePoints = 200 ):
##                timeValues = self.getTimeValues( totalTimeInterval, timePoints );
##                position = self.height - position;
##                displacementValues = [ ];
##                
##                for i in range( 0, len( timeValues ) ):
##                        initialDisplacementValue = ( ( self.tao_0 * ( 1.0 - 2.0 * self.ni_u ) * ( self.height - position ) ) /
##                                                     ( 2.0 * self.G * ( 1.0 - self.ni_u ) ) );
##                        summationResult = 0;
##
##                        for j in range( 0, numberOfSummationTerms ):
##                                term_1 = 1.0 / ( ( 2.0 * j + 1.0 ) ** 2 );
##                                term_2 = ( math.exp( - ( ( self.c * timeValues[ i ] * ( math.pi ** 2.0 ) * ( ( 2.0 * j + 1.0 ) ** 2.0 ) ) /
##                                                         ( 4.0 * ( self.height ** 2.0 ) ) ) ) );
##                                term_3 = math.cos( ( math.pi * position * ( 2.0 * j + 1.0 ) ) / ( 2 * self.height ) );
##                                summationResult += term_1 * term_2 * term_3;
##
##                        displacementValue = - ( initialDisplacementValue + self.c_m * self.gama * self.tao_0 *
##                                              ( ( self.height - position ) - ( 8.0 * self.height / ( math.pi ** 2.0 ) ) * summationResult ) );
##                        displacementValues.append( displacementValue );
##
##                return displacementValues;


        def getDisplacementValuesConstPosition( self, position, totalTimeInterval, numberOfSummationTerms = 200, timePoints = 200 ):
                timeValues = self.getTimeValues( totalTimeInterval, timePoints );
                displacementValues = [ ];

                for i in range( 0, len( timeValues ) ):
                        displacementValue = self.getDisplacementValue( position, timeValues[ i ], numberOfSummationTerms );
                        displacementValues.append( displacementValue );

                return displacementValues;


        def getDisplacementValuesNormalizedConstPosition( self, position, totalTimeInterval, numberOfSummationTerms = 200, timePoints = 200 ): # ( v - v_inicial ) / ( v_final - v_inicial )
                displacementValues = self.getDisplacementValuesConstPosition( position, totalTimeInterval, numberOfSummationTerms, timePoints );
                position = self.height - position;
                initialDisplacementValue = ( ( self.tao_0 * ( 1.0 - 2.0 * self.ni_u ) * ( self.height - position ) ) /
                                             ( 2.0 * self.G * ( 1.0 - self.ni_u ) ) );
                finalDisplacementValue = initialDisplacementValue + self.c_m * self.gama * self.tao_0 * ( self.height - position );
                displacementValuesNormalized = [ ];
                
                for i in range( 0, len( displacementValues ) ):
                        displacementValueNormalized = ( ( - displacementValues[ i ] - initialDisplacementValue ) /
                                                        ( finalDisplacementValue - initialDisplacementValue ) );
                        displacementValuesNormalized.append( displacementValueNormalized );

                return displacementValuesNormalized;
                

# EXAMPLE =======================================================================================

import matplotlib.pyplot as plt

height = 5.0
tao_0 = 1.0e+6
permeability = 1.0e-15
phi = 0.19
mi = 0.001
K = 8.0e+9
K_s = 3.6e+10
K_f = 3.3e+9
G = 6.0e+9
K_phi = 3.6e+10

if __name__ == '__main__':
        example = TerzaghisProblemAnalytical( height, tao_0, permeability, phi, mi, K, K_s, K_f, G, K_phi );
        AxisY = example.getPositionValues();
        AxisYNormalized = example.getPositionValuesNormalized();


##        plt.figure();
##        
##        Pressure05Time = o.getPressureValuesConstTime( 1.0 );
##        Pressure1Time = o.getPressureValuesConstTime( 5.0 );
##        Pressure2Time = o.getPressureValuesConstTime( 10.0 );
##        Pressure3Time = o.getPressureValuesConstTime( 25.0 );
##        Pressure4Time = o.getPressureValuesConstTime( 50.0 );
##        Pressure5Time = o.getPressureValuesConstTime( 100.0 );
##        
##        Plot1 = plt.plot( Pressure05Time, AxisY, 'k',
##                          Pressure1Time, AxisY, 'k',
##                          Pressure2Time, AxisY, 'k',
##                          Pressure3Time, AxisY, 'k',
##                          Pressure4Time, AxisY, 'k',
##                          Pressure5Time, AxisY, 'k');
##
##        Plot1 = plt.xlabel( 'Pressure (Pa)' );
##        Plot1 = plt.ylabel( 'y (m)' );


##        plt.figure();
##        
##        Pressure05TimeNormalized = o.getPressureValuesNormalizedConstTime( 1.0 );
##        Pressure1TimeNormalized = o.getPressureValuesNormalizedConstTime( 5.0 );
##        Pressure2TimeNormalized = o.getPressureValuesNormalizedConstTime( 10.0 );
##        Pressure3TimeNormalized = o.getPressureValuesNormalizedConstTime( 25.0 );
##        Pressure4TimeNormalized = o.getPressureValuesNormalizedConstTime( 50.0 );
##        Pressure5TimeNormalized = o.getPressureValuesNormalizedConstTime( 100.0 );
##
##        Plot2 = plt.plot( Pressure05TimeNormalized, AxisYNormalized, 'b',
##                          Pressure1TimeNormalized, AxisYNormalized, 'b',
##                          Pressure2TimeNormalized, AxisYNormalized, 'b',
##                          Pressure3TimeNormalized, AxisYNormalized, 'b',
##                          Pressure4TimeNormalized, AxisYNormalized, 'b',
##                          Pressure5TimeNormalized, AxisYNormalized, 'b');
##
##        Plot2 = plt.xlabel( 'p/p0' );
##        Plot2 = plt.ylabel( 'y/H' );


##        plt.figure();
##
##        Displacement0Time = o.getDisplacementValuesConstTime( 0.0 );
##        Displacement1Time = o.getDisplacementValuesConstTime( 5.0 );
##        Displacement2Time = o.getDisplacementValuesConstTime( 10.0 );
##        Displacement3Time = o.getDisplacementValuesConstTime( 25.0 );
##        Displacement4Time = o.getDisplacementValuesConstTime( 50.0 );
##        Displacement5Time = o.getDisplacementValuesConstTime( 100.0 );
##
##        Plot3 = plt.plot( Displacement0Time, AxisY, 'k',
##                          Displacement1Time, AxisY, 'k',
##                          Displacement2Time, AxisY, 'k',
##                          Displacement3Time, AxisY, 'k',
##                          Displacement4Time, AxisY, 'k',
##                          Displacement5Time, AxisY, 'k');
##
##        Plot3 = plt.xlabel( 'Displacement (m)' );
##        Plot3 = plt.ylabel( 'y (m)' );


##        plt.figure();
##
##        Displacement1TimeNormalized = o.getDisplacementValuesNormalizedConstTime( 0.0 );
##        Displacement2TimeNormalized = o.getDisplacementValuesNormalizedConstTime( 5.0 );
##        Displacement3TimeNormalized = o.getDisplacementValuesNormalizedConstTime( 10.0 );
##        Displacement5TimeNormalized = o.getDisplacementValuesNormalizedConstTime( 25.0 );
##        Displacement10TimeNormalized = o.getDisplacementValuesNormalizedConstTime( 50.0 );
##        Displacement20TimeNormalized = o.getDisplacementValuesNormalizedConstTime( 100.0 );
##
##        Plot4 = plt.plot( Displacement1TimeNormalized, AxisYNormalized, 'b',
##                          Displacement2TimeNormalized, AxisYNormalized, 'b',
##                          Displacement3TimeNormalized, AxisYNormalized, 'b',
##                          Displacement5TimeNormalized, AxisYNormalized, 'b',
##                          Displacement10TimeNormalized, AxisYNormalized, 'b',
##                          Displacement20TimeNormalized, AxisYNormalized, 'b');
##
##        Plot4 = plt.xlabel( '(v - v_inicial)/(v_final - v_inicial)' );
##        Plot4 = plt.ylabel( 'y/H' );


        timeInterval = 1000.0;
        timeValues = example.getTimeValues( timeInterval );


##        plt.figure();
##
##        Pressure0Position = o.getPressureValuesConstPosition( 0.0, timeInterval );
##        Pressure3Position = o.getPressureValuesConstPosition( 3.0, timeInterval );
##
##        Plot5 = plt.plot( timeValues, Pressure0Position, 'k',
##                          timeValues, Pressure3Position, 'b');
##
##        Plot5 = plt.xlabel( 'time (s)' );
##        Plot5 = plt.ylabel( 'pressure (Pa)' );


##        plt.figure();
##
##        Pressure0PositionNormalized = o.getPressureValuesNormalizedConstPosition( 0.0, timeInterval );
##        Pressure3PositionNormalized = o.getPressureValuesNormalizedConstPosition( 3.0, timeInterval );
##
##        Plot6 = plt.plot( timeValues, Pressure0PositionNormalized, 'k',
##                          timeValues, Pressure3PositionNormalized, 'b');
##
##        Plot6 = plt.xlabel( 'time (s)' );
##        Plot6 = plt.ylabel( 'p/p_0' );


##        plt.figure();
##
##        Displacement6Position = o.getDisplacementValuesConstPosition( 6.0, timeInterval );
##
##        Plot7 = plt.plot( timeValues, Displacement6Position, 'k' );
##
##        Plot7 = plt.xlabel( 'time (s)' );
##        Plot7 = plt.ylabel( 'displacement (m)' );


##        plt.figure();
##
##        Displacement6PositionNormalized = o.getDisplacementValuesNormalizedConstPosition( 6.0, timeInterval );
##
##        Plot7 = plt.plot( timeValues, Displacement6PositionNormalized, 'k' );
##
##        Plot7 = plt.xlabel( 'time (s)' );
##        Plot7 = plt.ylabel( '(v - v_inicial)/(v_final - v_inicial)' );


        plt.show();
