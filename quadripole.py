import matplotlib.pyplot as plt
import numpy as np

class quadripole:
    """
    Simple quadripole for circuit manipulation.
    """

    def __init__(self, **kwargs):
        # print(kwargs)
        self.Z0 = 50
        self.mode = 'db'
        
        if "Z0" in kwargs:
            self.Z0 = kwargs['Z0']

        if "mode" in kwargs:
            self.mode = kwargs['Z0']

        if "z" in kwargs:
            self.set_z(kwargs['z'])
            self.z_to_y()
            self.z_to_ABCD()
            self.z_to_S(Z0=50)
        elif "y" in kwargs:
            self.set_y(kwargs['y'])
            self.y_to_z()
            self.y_to_ABCD()
            self.y_to_S(Z0=50)
        elif "ABCD" in kwargs:
            self.set_ABCD(kwargs['ABCD'])
            self.ABCD_to_z()
            self.ABCD_to_y()
            self.ABCD_to_S(Z0=50)
        elif "S" in kwargs:
            self.set_S(kwargs['S'])
            self.S_to_z_()
            self.S_to_y_()
            self.S_to_ABCD_()
        else:
            raise TypeError( "must provide z= or y= or ABCD= or S= parameter values" )
        
    
    def set_z(self, z, mode='db'):
        if self.mode == 'db':
            z = 10**(z/20)
        self.z11 = z[0][0]
        self.z12 = z[0][1]
        self.z21 = z[1][0]
        self.z22 = z[1][1]

    def z(self):
        return np.array([[ self.z11, self.z12 ], [ self.z21, self.z22 ]])
    
    def serie(self, qDevice):
        temp_z11 = self.z11 + qDevice.z11
        temp_z12 = self.z12 + qDevice.z12
        temp_z21 = self.z21 + qDevice.z21
        temp_z22 = self.z22 + qDevice.z22
        return quadripole(z = np.array([[ temp_z11, temp_z12 ], [ temp_z21, temp_z22 ]]))

    def z_to_y(self):
        Z = self.z11 * self.z22 - self.z12 * self.z21
        self.y11 =  self.z22/abs(Z)
        self.y12 = -self.z12/abs(Z)
        self.y21 = -self.z21/abs(Z)
        self.y22 =  self.z11/abs(Z)
    
    def z_to_ABCD(self):
        self.A = self.z11/self.z21
        self.B = (self.z11 * self.z22 + self.z12 * self.z21)/self.z21
        self.C = 1/self.z21
        self.D = self.z22/self.z21
    
    def z_to_S(self, Z0=50):
        Z0 = self.Z0
        
        Delta_1 = (((self.z11/Z0) + 1)*((self.z22/Z0) + 1) - ((self.z12/Z0)*(self.z21/Z0)))
        self.S11 = (((self.z11/Z0) - 1)*((self.z22/Z0) + 1) - ((self.z12/Z0)*(self.z21/Z0)))/Delta_1
        self.S12 = 2*(self.z12/Z0)/Delta_1
        self.S21 = 2*(self.z21/Z0)/Delta_1
        self.S22 = (((self.z11/Z0) + 1)*((self.z22/Z0) - 1) - ((self.z12/Z0)*(self.z21/Z0)))/Delta_1

    def set_y(self, y):
        if self.mode == 'db':
            y = 10**(y/20)
        self.y11 = y[0][0]
        self.y12 = y[0][1]
        self.y21 = y[1][0]
        self.y22 = y[1][1]
    
    def y(self):
        return np.array([[ self.y11, self.y12 ], [ self.y21, self.y22 ]])

    def shunt(self, qDevice):
        temp_y11 = self.y11 + qDevice.y11
        temp_y12 = self.y12 + qDevice.y12
        temp_y21 = self.y21 + qDevice.y21
        temp_y22 = self.y22 + qDevice.y22

        return quadripole(y = np.array([[ temp_y11, temp_y12 ], [ temp_y21, temp_y22 ]]))
    
    def y_to_z(self):
        Y = self.y11 * self.y22 - self.y12 * self.y21
        self.z11 =  self.y22/abs(Y)
        self.z12 = -self.y12/abs(Y)
        self.z21 = -self.y21/abs(Y)
        self.z22 =  self.y11/abs(Y)
    
    def y_to_ABCD(self):
        self.A = -self.y22/self.y21
        self.B = -1/self.y21
        self.C =  (self.y11 * self.y22 + self.y12 * self.y21)/self.y21
        self.D = -self.y11/self.y21
    
    def y_to_S(self, Z0=50):
        Z0 = self.Z0
        Delta_2 = ((1 + (self.y11*Z0))*(1 + (self.y22*Z0)) - ((self.y12*Z0)*(self.y21*Z0)))
        self.S11 =  ((1 - (self.y11*Z0))*(1 + (self.y22*Z0)) + ((self.y12*Z0)*(self.y21*Z0)))/Delta_2
        self.S12 = -2*(self.y12*Z0)/Delta_2
        self.S21 = -2*(self.y21*Z0)/Delta_2
        self.S22 =  ((1 + (self.y11*Z0))*(1 - (self.y22*Z0)) + ((self.y12*Z0)*(self.z21*Z0)))/Delta_2

    def set_ABCD(self, ABCD, mode='db'):
        if self.mode == 'db':
            ABCD = 10**(ABCD/20)
        self.A = ABCD[0][0]
        self.B = ABCD[0][1]
        self.C = ABCD[1][0]
        self.D = ABCD[1][1]
    
    def ABCD(self):
        return np.array([[ self.A, self.B ], [ self.C, self.D ]])

    def cascade(self, qDevice):
        temp_A = self.A * qDevice.A + self.B * qDevice.C
        temp_B = self.A * qDevice.B + self.B * qDevice.D
        temp_C = self.C * qDevice.A + self.D * qDevice.C
        temp_D = self.C * qDevice.B + self.D * qDevice.D
        return quadripole(ABCD = np.array([[ temp_A, temp_B ], [ temp_C, temp_D ]]))
    
    def ABCD_to_z(self):
        self.z11 = self.A/self.C
        self.z12 = (self.A * self.D - self.B * self.C)/self.C
        self.z21 = 1/self.C
        self.z22 = self.D/self.C
    
    def ABCD_to_y(self):
        self.y11 =  self.D/self.B
        self.y12 = -(self.A * self.D - self.B * self.C)/self.B
        self.y21 = -1/self.B
        self.y22 =  self.A/self.B
    
    def ABCD_to_S(self, Z0=50):
        Z0 = self.Z0

        A_ = self.A
        B_ = self.B/Z0
        C_ = self.C*Z0
        D_ = self.D
        
        Delta_4 = A_ + B_ + C_ + D_
        self.S11 =  (A_ + B_ - C_ - D_ )/Delta_4
        self.S12 =  2*(A_*D_ - B_*C_)/Delta_4
        self.S21 =  2/Delta_4
        self.S22 = (-A_ + B_ - C_ + D_)/Delta_4
    
    def set_S(self, S, mode='db'):
        if self.mode == 'db':
            S = 10**(S/20)
        self.S11 = S[0][0]
        self.S21 = S[0][1]
        self.S12 = S[1][0]
        self.S22 = S[1][1]

    def S(self):
        return np.array([[ self.S11, self.S12 ], [ self.S21, self.S22 ]])
    
    def S_to_z_(self):
        Delta_5 = ((1 - self.S11)*(1 - self.S22)) - self.S12 * self.S21
        self.z11 = (((1 + self.S11) * (1 - self.S22)) + self.S12 * self.S21)/Delta_5
        self.z12 = 2*self.S12/Delta_5
        self.z21 = 2*self.S21/Delta_5
        self.z22 = (((1 - self.S11) * (1 + self.S22)) + self.S12 * self.S21)/Delta_5
    
    def S_to_y_(self):
        Delta_6 = ((1 + self.S11)*(1 + self.S22)) - self.S12 * self.S21
        self.y11 =  (((1 - self.S11) * (1 + self.S22)) + self.S12 * self.S21)/Delta_6
        self.y12 = -2*self.S12/Delta_6
        self.y21 = -2*self.S21/Delta_6
        self.y22 =  (((1 + self.S11) * (1 - self.S22)) + self.S12 * self.S21)/Delta_6
    
    def S_to_ABCD_(self):
        self.A = (((1 + self.S11) * (1 - self.S22)) + self.S12 * self.S21)/(2*self.S21)
        self.B = (((1 + self.S11) * (1 + self.S22)) - self.S12 * self.S21)/(2*self.S21)
        self.C = (((1 - self.S11) * (1 - self.S22)) - self.S12 * self.S21)/(2*self.S21)
        self.D = (((1 - self.S11) * (1 + self.S22)) + self.S12 * self.S21)/(2*self.S21)