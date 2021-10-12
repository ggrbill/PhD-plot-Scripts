# ABREVIATIONS USED =============================================================================

# PROPERTIES OF THE UPPER PART

# height_1 - Height
# permeability_1 - Reference permeability
# phi_1 - Reference porosity
# K_1 - Bulk modulus
# K_s_1 - Solid bulk modulus
# G_1 - Sheer modulus
# K_phi_1 - Unjacket pore compressibility

# H_1 - Poroelastic expansion coefficient
# R_1 - Biot modulus
# alpha_1 - Biot-Willis coefficient
# K_p_1 - Drained pore compressibility
# K_u_1 - Undrained bulk modulus
# B_1 - Skempton's coefficient
# ni_1 - Drained Poisson's ratio
# ni_u_1 - Undrained Poisson's ratio
# K_ni_u_1 - Uniaxial undrained bulk modulus
# c_s_1 - Solid phase compressibility
# m_1 - Confined compressibility
# gama_1 - Loading efficiency
# c_1 - Consolidation coefficient / Hydraulic diffusivity
# t_1 - Consolidation time

# PROPERTIES OF THE LOWER PART

# height_2 - Height
# permeability_2 - Reference permeability
# phi_2 - Reference porosity
# K_2 - Bulk modulus
# K_s_2 - Solid bulk modulus
# G_2 - Sheer modulus
# K_phi_2 - Unjacket pore compressibility

# H_2 - Poroelastic expansion coefficient
# R_2 - Biot modulus
# alpha_2 - Biot-Willis coefficient
# K_p_2 - Drained pore compressibility
# K_u_2 - Undrained bulk modulus
# B_2 - Skempton's coefficient
# ni_2 - Drained Poisson's ratio
# ni_u_2 - Undrained Poisson's ratio
# K_ni_u_2 - Uniaxial undrained bulk modulus
# c_s_2 - Solid phase compressibility
# m_2 - Confined compressibility
# gama_2 - Loading efficiency
# c_2 - Consolidation coefficient / Hydraulic diffusivity
# t_2 - Consolidation time

# PROPERTIES OF THE FLUID

# mi - Viscosity
# K_f - Fluid bulk modulus

# c_f - Fluid phase compressibility
# p_0_1 - Initial pore pressure in the upper part
# p_0_2 - Initial pore pressure in the lower part

# GENERAL DATA

# tao_0 - Normal stress
# beta - Ratio between the consolidation times
# w - Ratio between the compressibilities and the permeabilities


import math;


# CLASS DEFINITION ==============================================================================

class TwoLayeredSoilAnalytical( object ):

        # Constructor ---------------------------------------------------------------------------
        def __init__( self, height_1, permeability_1, phi_1, K_1, K_s_1, G_1, K_phi_1,
                      height_2, permeability_2, phi_2, K_2, K_s_2, G_2, K_phi_2,
                      mi, K_f, tao_0, p_0_1 = 0, p_0_2 = 0 ):

                self.tao_0 = tao_0;

                self.mi = mi;
                self.K_f = K_f;

                self._calculate_c_f();
                
                self.height_1 = height_1;
                self.permeability_1 = permeability_1;
                self.phi_1 = phi_1;
                self.K_1 = K_1;
                self.K_s_1 = K_s_1;
                self.G_1 = G_1;
                self.K_phi_1 = K_phi_1;

                self.H_1 = self._calculate_H( self.K_1, self.K_s_1 );
                self.R_1 = self._calculate_R( self.H_1, self.phi_1, self.K_f, self.K_phi_1 );
                self.alpha_1 = self._calculate_alpha( self.K_1, self.K_s_1 );
                self.K_p_1 = self._calculate_K_p( self.phi_1, self.K_1, self.alpha_1 );
                self.B_1 = self._calculate_B( self.R_1, self.H_1 );
                self.K_u_1 = self._calculate_K_u( self.K_1, self.alpha_1, self.B_1 );
                self.ni_1 = self._calculate_ni( self.K_1, self.G_1 );
                self.ni_u_1 = self._calculate_ni_u( self.ni_1, self.alpha_1, self.B_1 );
                self.K_ni_u_1 = self._calculate_K_ni_u( self.K_u_1, self.ni_u_1 );
                self.c_s_1 = self._calculate_c_s( self.K_s_1 );
                self.m_1 = self._calculate_m( self.K_1, self.G_1 );
                self.gama_1 = self._calculate_gama( self.B_1, self.ni_u_1 );
                self.c_1 = self._calculate_c( self.permeability_1, self.G_1, self.ni_1, self.ni_u_1, self.mi, self.alpha_1 );
                self.t_1 = self._calculate_t( self.height_1, self.c_1 );
                
                self.height_2 = height_2;
                self.permeability_2 = permeability_2;
                self.phi_2 = phi_2;
                self.K_2 = K_2;
                self.K_s_2 = K_s_2;
                self.G_2 = G_2;
                self.K_phi_2 = K_phi_2;

                self.H_2 = self._calculate_H( self.K_2, self.K_s_2 );
                self.R_2 = self._calculate_R( self.H_2, self.phi_2, self.K_f, self.K_phi_2 );
                self.alpha_2 = self._calculate_alpha( self.K_2, self.K_s_2 );
                self.K_p_2 = self._calculate_K_p( self.phi_2, self.K_2, self.alpha_2 );
                self.B_2 = self._calculate_B( self.R_2, self.H_2 );
                self.K_u_2 = self._calculate_K_u( self.K_2, self.alpha_2, self.B_2 );
                self.ni_2 = self._calculate_ni( self.K_2, self.G_2 );
                self.ni_u_2 = self._calculate_ni_u( self.ni_2, self.alpha_2, self.B_2 );
                self.K_ni_u_2 = self._calculate_K_ni_u( self.K_u_2, self.ni_u_2 );
                self.c_s_2 = self._calculate_c_s( self.K_s_2 );
                self.m_2 = self._calculate_m( self.K_2, self.G_2 );
                self.gama_2 = self._calculate_gama( self.B_2, self.ni_u_2 );
                self.c_2 = self._calculate_c( self.permeability_2, self.G_2, self.ni_2, self.ni_u_2, self.mi, self.alpha_2 );
                self.t_2 = self._calculate_t( self.height_2, self.c_2 );

                if p_0_1 == 0:
                        self.p_0_1 = self._calculate_p_0( self.gama_1, self.tao_0 );
                        self.p_0_2 = self._calculate_p_0( self.gama_2, self.tao_0 );
                else:
                        self.p_0_1 = p_0_1;
                        self.p_0_2 = p_0_2;

                self._calculate_beta();
                self._calculate_w();


        # Internal functions --------------------------------------------------------------------
        def _calculate_c_f( self ):
                self.c_f = 1.0 / self.K_f;

        def _calculate_H( self, K, K_s ):
                H = 1.0 / ( ( 1.0 / K ) - ( 1.0 / K_s ) );
                return H;

        def _calculate_R( self, H, phi, K_f, K_phi ):
                R = 1.0 / ( ( 1.0 / H ) + phi * ( ( 1.0 / K_f ) - ( 1.0 / K_phi ) ) );
                return R;

        def _calculate_alpha( self, K, K_s ):
                alpha = 1.0 - ( K / K_s );
                return alpha;

        def _calculate_K_p( self, phi, K, alpha ):
                K_p = phi * K / alpha;
                return K_p;

        def _calculate_B( self, R, H ):
                B = R / H;
                return B;

        def _calculate_K_u( self, K, alpha, B ):
                K_u = K / ( 1.0 - alpha * B );
                return K_u;

        def _calculate_ni( self, K, G ):
                ni = ( 3.0 * K - 2.0 * G ) / ( 2.0 * ( 3.0 * K + G ) );
                return ni;

        def _calculate_ni_u( self, ni, alpha, B ):
                ni_u = ( ( 3.0 * ni + alpha * B * ( 1.0 - 2.0 * ni ) ) / ( 3.0 - alpha * B * ( 1.0 - 2.0 * ni ) ) );
                return ni_u;

        def _calculate_K_ni_u( self, K_u, ni_u ):
                K_ni_u = ( 3.0 * K_u * ( 1.0 - ni_u ) ) / ( 1.0 + ni_u );
                return K_ni_u;

        def _calculate_c_s( self, K_s ):
                c_s = 1.0 / K_s;
                return c_s;
        
        def _calculate_m( self, K, G ):
                m = 1.0 / ( K + G * (4.0 / 3.0) );
                return m;
        
        def _calculate_gama( self, B, ni_u ):
                gama = ( B * ( 1.0 + ni_u ) ) / ( 3.0 * ( 1.0 - ni_u ) );
                return gama;

        def _calculate_c( self, permeability, G, ni, ni_u, mi, alpha ):
                c = ( ( 2.0 * permeability * G * ( 1.0 - ni ) * ( ni_u - ni ) ) /
                           ( mi * ( alpha ** 2.0 ) * ( 1.0 - ni_u ) * ( ( 1.0 - 2.0 * ni ) ** 2.0 ) ) );
                return c;

        def _calculate_t( self, height, c ):
                t = ( height ** 2 ) / c;
                return t;

        def _calculate_p_0( self, gama, tao_0 ):
                p_0 = gama * tao_0;
                return p_0;

        def _calculate_beta( self ):
                self.beta = math.sqrt( self.t_1 / self.t_2 );

        def _calculate_w( self ):
                self.w = math.sqrt( self.permeability_2 * self.m_2 ) / math.sqrt( self.permeability_1 * self.m_1 );


        def _calculateFunctionToFindTheRoots( self, x ):
                y = - self.w * math.sin( self.beta * x ) * math.sin( x ) + math.cos( self.beta * x ) * math.cos( x );
                return y;


        def _calculateRoots( self, numberOfRoots, maxIterations = 100, increment = 0.001 ):
                roots = [ ];
                
                while len( roots ) < numberOfRoots:
                        if len( roots ) == 0:
                                A = 0;
                        else:
                                if self._calculateFunctionToFindTheRoots( B ) != 0:
                                        A = B;
                                else:
                                        A = B + increment;
                                
                        B = A + increment;

                        y_A = self._calculateFunctionToFindTheRoots( A );
                        y_B = self._calculateFunctionToFindTheRoots( B );

                        while y_A * y_B > 0:
                                A = B;
                                B = A + increment;
                                y_A = self._calculateFunctionToFindTheRoots( A );
                                y_B = self._calculateFunctionToFindTheRoots( B );

                        if y_B == 0:
                                roots.append( B );
                        else:
                                C = A;
                                D = B;
                                E = ( C + D ) / 2;
                                y_E = self._calculateFunctionToFindTheRoots( E );

                                iteration = 0;
                                while iteration < maxIterations and y_E != 0:
                                        y_C = self._calculateFunctionToFindTheRoots( C );
                                        y_E = self._calculateFunctionToFindTheRoots( E );

                                        if y_C * y_E < 0:
                                                D = E;
                                        else:
                                                C = E;

                                        E = ( C + D ) / 2;
                                        iteration += 1;

                                roots.append( E );

                return roots;


        def _calculateCommonDivisors( self, roots ):
                commonDivisors = [ ];

                for i in range( 0, len( roots ) ):
                        term_1 = ( 1.0 + self.w * self.beta ) * math.cos( self.beta * roots[ i ] ) * math.sin( roots[ i ] );
                        term_2 = ( self.w + self.beta ) * math.sin( self.beta * roots[ i ] ) * math.cos( roots[ i ] );
                        commonDivisor = roots[ i ] * ( term_1 + term_2 );
                        commonDivisors.append( commonDivisor );

                return commonDivisors;                
                

        # Class interface -----------------------------------------------------------------------
        def getPositionValues( self, ny = 200 ):
                dy = ( self.height_1 + self.height_2 ) / ( ny - 1.0 );
                positionValues = [ ];

                for i in range( 0, ny ):
                        positionValues.append( i * dy );
                
                return positionValues;


        def getPositionValuesNormalized( self, ny = 200 ):
                positionValues = self.getPositionValues( ny );
                positionValuesNormalized = [ ];

                for i in range( 0, len( positionValues ) ):
                        positionValuesNormalized.append( positionValues[ i ] / ( self.height_1 + self.height_2 ) );

                return positionValuesNormalized;


        def getPressureValue( self, yPosition, time, numberOfSummationTerms = 200, roots = [ ], commonDivisors = [ ] ):
                position = yPosition - self.height_2;
                                          
                if len( commonDivisors ) == 0:
                        roots = self._calculateRoots( numberOfSummationTerms );
                        commonDivisors = self._calculateCommonDivisors( roots );

##                commonDivisors = [ ];
##
##                for i in range( 0, len( roots ) ):
##                        term_1 = ( 1.0 + self.w * self.beta ) * math.cos( self.beta * roots[ i ] ) * math.sin( roots[ i ] );
##                        term_2 = ( self.w + self.beta ) * math.sin( self.beta * roots[ i ] ) * math.cos( roots[ i ] );
##                        commonDivisor = roots[ i ] * ( term_1 + term_2 );
##                        commonDivisors.append( commonDivisor );

                summationResult = 0;

                if position <= 0:
                        for j in range( 0, numberOfSummationTerms ):
                                term_1 = math.cos( roots[ j ] ) * math.cos( roots[ j ] * position / self.height_2 );
                                term_2 = math.sin( roots[ j ] ) * math.sin( roots[ j ] * position / self.height_2 );
                                term_3 = math.exp( - ( roots[ j ] ** 2 ) * time / self.t_2 );
                                summationResult += term_3 * ( term_1 - term_2 ) / commonDivisors[ j ];
                else:
                        for j in range( 0, numberOfSummationTerms ):
                                term_1 = math.cos( roots[ j ] ) * math.cos( self.beta * roots[ j ] * position / self.height_1 );
                                term_2 = self.w * math.sin( roots[ j ] ) * math.sin( self.beta * roots[ j ] * position / self.height_1 );
                                term_3 = math.exp( - ( roots[ j ] ** 2 ) * time / self.t_2 );
                                summationResult += term_3 * ( term_1 - term_2 ) / commonDivisors[ j ];

                pressureValue = 2.0 * self.p_0_2 * summationResult;
                
                return pressureValue;


##        def getPressureValuesConstTime( self, time, numberOfSummationTerms = 200, ny = 200 ):
##                positionValues = self.getPositionValues( ny );
##                for i in range( 0, len( positionValues ) ):
##                        positionValues[ i ] = positionValues[ i ] - self.height_2;
##
##                roots = self._calculateRoots( numberOfSummationTerms );
##
##                commonDivisors = [ ];
##                
##                for i in range( 0, len( roots ) ):
##                        term_1 = ( 1.0 + self.w * self.beta ) * math.cos( self.beta * roots[ i ] ) * math.sin( roots[ i ] );
##                        term_2 = ( self.w + self.beta ) * math.sin( self.beta * roots[ i ] ) * math.cos( roots[ i ] );
##                        commonDivisor = roots[ i ] * ( term_1 + term_2 );
##                        commonDivisors.append( commonDivisor );
##
##                pressureValues = [ ];
##
##                for i in range( 0, len( positionValues ) ):
##                        
##                        if positionValues[ i ] <= 0:
##                                summationResult = 0;
##                                
##                                for j in range( 0, numberOfSummationTerms ):
##                                        term_1 = math.cos( roots[ j ] ) * math.cos( roots[ j ] * positionValues[ i ] / self.height_2 );
##                                        term_2 = math.sin( roots[ j ] ) * math.sin( roots[ j ] * positionValues[ i ] / self.height_2 );
##                                        term_3 = math.exp( - ( roots[ j ] ** 2 ) * time / self.t_2 );
##                                        summationResult += term_3 * ( term_1 - term_2 ) / commonDivisors[ j ];
##
##                                pressureValue = 2.0 * self.p_0_2 * summationResult;
##                                pressureValues.append( pressureValue );
##
##                        if positionValues[ i ] > 0:
##                                summationResult = 0;
##
##                                for j in range( 0, numberOfSummationTerms ):
##                                        term_1 = math.cos( roots[ j ] ) * math.cos( self.beta * roots[ j ] * positionValues[ i ] / self.height_1 );
##                                        term_2 = self.w * math.sin( roots[ j ] ) * math.sin( self.beta * roots[ j ] * positionValues[ i ] / self.height_1 );
##                                        term_3 = math.exp( - ( roots[ j ] ** 2 ) * time / self.t_2 );
##                                        summationResult += term_3 * ( term_1 - term_2 ) / commonDivisors[ j ];
##
##                                pressureValue = 2.0 * self.p_0_2 * summationResult;
##                                pressureValues.append( pressureValue );
##
##                return pressureValues;


        def getPressureValuesConstTime( self, time, numberOfSummationTerms = 200, ny = 200 ):
                if time == 0.0:
                    numberOfSummationTerms = 10000
            
                positionValues = self.getPositionValues( ny );
                roots = self._calculateRoots( numberOfSummationTerms );
                commonDivisors = self._calculateCommonDivisors( roots );
                pressureValues = [ ];

                for i in range( 0, len( positionValues ) ):
                        pressureValue = self.getPressureValue( positionValues[ i ], time, numberOfSummationTerms, roots, commonDivisors );
                        pressureValues.append( pressureValue );

                return pressureValues;


        def getPressureValuesNormalizedConstTime( self, time, numberOfSummationTerms = 200, ny = 200 ): # p / p_0
                pressureValues = self.getPressureValuesConstTime( time, numberOfSummationTerms, ny);
                pressureValuesNormalized = [ ];
                
                positionValues = self.getPositionValues( ny );

                for i in range( 0, len( pressureValues ) ):
                        if positionValues[ i ] < self.height_2:
                                pressureValuesNormalized.append( pressureValues[ i ] / self.p_0_2 );
                        else:
                                if positionValues[ i ] == self.height_2:
                                        pressureValuesNormalized.append( pressureValues[ i ] / ( ( self.p_0_1 + self.p_0_2 ) / 2 ) );
                                else:
                                        pressureValuesNormalized.append( pressureValues[ i ] / self.p_0_2 );

                return pressureValuesNormalized;


        def getTimeValues( self, totalTimeInterval, timePoints = 200 ):
                dt = totalTimeInterval / ( timePoints - 1 );
                timeValues = [ ];

                for i in range( 0, timePoints ):
                        timeValues.append( i * dt );

                return timeValues;                


##        def getPressureValuesConstPosition( self, position, totalTimeInterval, numberOfSummationTerms = 200, timePoints = 200 ):
##                timeValues = self.getTimeValues( totalTimeInterval, timePoints );
##                position = position - self.height_2;
##
##                roots = self._calculateRoots( numberOfSummationTerms );
##
##                commonDivisors = [ ];
##                
##                for i in range( 0, len( roots ) ):
##                        term_1 = ( 1.0 + self.w * self.beta ) * math.cos( self.beta * roots[ i ] ) * math.sin( roots[ i ] );
##                        term_2 = ( self.w + self.beta ) * math.sin( self.beta * roots[ i ] ) * math.cos( roots[ i ] );
##                        commonDivisor = roots[ i ] * ( term_1 + term_2 );
##                        commonDivisors.append( commonDivisor );
##
##                pressureValues = [ ];
##
##                for i in range( 0, len( timeValues ) ):
##
##                        if position <= 0:
##                                summationResult = 0;
##                                
##                                for j in range( 0, numberOfSummationTerms ):
##                                        term_1 = math.cos( roots[ j ] ) * math.cos( roots[ j ] * position / self.height_2 );
##                                        term_2 = math.sin( roots[ j ] ) * math.sin( roots[ j ] * position / self.height_2 );
##                                        term_3 = math.exp( - ( roots[ j ] ** 2 ) * timeValues[ i ] / self.t_2 );
##                                        summationResult += term_3 * ( term_1 - term_2 ) / commonDivisors[ j ];
##
##                                pressureValue = 2.0 * self.p_0_2 * summationResult;
##                                pressureValues.append( pressureValue );
##
##                        if position > 0:
##                                summationResult = 0;
##
##                                for j in range( 0, numberOfSummationTerms ):
##                                        term_1 = math.cos( roots[ j ] ) * math.cos( self.beta * roots[ j ] * position / self.height_1 );
##                                        term_2 = self.w * math.sin( roots[ j ] ) * math.sin( self.beta * roots[ j ] * position / self.height_1 );
##                                        term_3 = math.exp( - ( roots[ j ] ** 2 ) * timeValues[ i ] / self.t_2 );
##                                        summationResult += term_3 * ( term_1 - term_2 ) / commonDivisors[ j ];
##
##                                pressureValue = 2.0 * self.p_0_2 * summationResult;
##                                pressureValues.append( pressureValue );
##
##                return pressureValues;


        def getPressureValuesConstPosition( self, position, totalTimeInterval, numberOfSummationTerms = 200, timePoints = 200 ):
                timeValues = self.getTimeValues( totalTimeInterval, timePoints );
                roots = self._calculateRoots( numberOfSummationTerms );
                commonDivisors = self._calculateCommonDivisors( roots );
                pressureValues = [ ];

                for i in range( 0, len( timeValues ) ):
                        pressureValue = self.getPressureValue( position, timeValues[ i ], numberOfSummationTerms, roots, commonDivisors );
                        pressureValues.append( pressureValue );

                return pressureValues;


        def getPressureValuesNormalizedConstPosition( self, position, totalTimeInterval, numberOfSummationTerms = 200, timePoints = 200 ): # p / p_0
                pressureValues = self.getPressureValuesConstPosition( position, totalTimeInterval, numberOfSummationTerms, timePoints );
                pressureValuesNormalized = [ ];

                for i in range( 0, len( pressureValues ) ):
                        if position < self.height_2:
                                pressureValuesNormalized.append( pressureValues[ i ] / self.p_0_2 );
                        else:
                                if position == self.height_2:
                                        pressureValuesNormalized.append( pressureValues[ i ] / ( ( self.p_0_1 + self.p_0_2 ) / 2 ) );
                                else:
                                        pressureValuesNormalized.append( pressureValues[ i ] / self.p_0_2 );

                return pressureValuesNormalized;


# EXAMPLE =======================================================================================

import matplotlib.pyplot as plt

if __name__ == '__main__':
        example = TwoLayeredSoilAnalytical( 3.0, 2.0e-15, 0.19, 8.0e9, 3.6e10, 6.0e9, 3.6e10,
                      9.0, 2.0e-16, 0.19, 8.0e9, 3.6e10, 6.0e9, 3.6e10, 0.001, 3.3e9, 1.0e6);
        AxisY = example.getPositionValues();
        AxisYNormalized = example.getPositionValuesNormalized();


##        plt.figure();
##
##        pressureConstTime = example.getPressureValuesConstTime( 300.0 );
##
##        plt.plot( pressureConstTime, AxisY, 'k' );
##
##        plt.xlabel( 'Pressure [Pa]' );
##        plt.ylabel( 'Position [m]' );
##        plt.grid( True );
##        plt.title( '300 [s]' );


##        plt.figure();
##
##        pressureNormalizedConstTime = example.getPressureValuesNormalizedConstTime( 700.0 );
##
##        plt.plot( pressureNormalizedConstTime, AxisYNormalized, 'b' );
##
##        plt.xlabel( 'p/p_0' );
##        plt.ylabel( 'y/H' );
##        plt.grid( True );


        timeInterval = 10000.0;
        timeValues = example.getTimeValues( timeInterval );


##        plt.figure();
##
##        pressureConstPosition00 = example.getPressureValuesConstPosition( 0.0, timeInterval );
##        pressureConstPosition08 = example.getPressureValuesConstPosition( 8.0, timeInterval );
##
##        plt.plot( timeValues, pressureConstPosition00, 'k', label = '0.0' );
##        plt.plot( timeValues, pressureConstPosition08, 'b', label = '8.0' );
##
##        plt.xlabel( 'Time [s]' );
##        plt.ylabel( 'Pressure [Pa]' );
##        plt.grid( True );
##        plt.legend( title = 'Position [m]', fontsize = 12 );


##        plt.figure();
##
##        pressureNormalizedConstPosition00 = example.getPressureValuesNormalizedConstPosition( 0.0, timeInterval );
##        pressureNormalizedConstPosition08 = example.getPressureValuesNormalizedConstPosition( 8.0, timeInterval );
##
##        plt.plot( timeValues, pressureNormalizedConstPosition00, 'k', label = '0.0' );
##        plt.plot( timeValues, pressureNormalizedConstPosition08, 'b', label = '8.0' );
##
##        plt.xlabel( 'Time [s]' );
##        plt.ylabel( 'p/p_0' );
##        plt.grid( True );
##        plt.legend( title = 'Position [m]', fontsize = 12 );

        
        plt.show();
