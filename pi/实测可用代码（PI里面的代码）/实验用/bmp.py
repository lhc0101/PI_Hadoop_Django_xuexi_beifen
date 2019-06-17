# -*- coding: utf-8 -*-
"""
BOSCH BMP180 Temperature and Air Pressure Sensor Operation
BMP180 datasheet: 
    https://www.bosch-sensortec.com/bst/products/all_products/bmp180
Platform:
    Raspbian-Jessie on Rapsberry Pi2
Dependencies: 
    Enable I2C bus by 'raspi-config'
Connections:
    Sensor - Raspberry Pi2 physical pin
    -----------------------------------
      SCL  -   5
      SDA  -   3
      VCC  -   1 (+3.3V)
      GND  -   9 ( GND )
Caution:
    BMP180 supply voltage must between 1.8V - 3.6V.
    Over voltage may damage your sensor.
    
Created on Tue Oct  9 08:35:10 2018
@author: Farman
"""
 
import smbus  # for i2c bus operation
import struct # for data repacking
 
 
class BMP180():
    def __init__(self, i2c_interface_id):
        '''
        i2c_interface_id : 
            use 'i2cdetect -a -y 1' in shell to check.
        '''
        self.bus  = smbus.SMBus(i2c_interface_id)         
        self.addr = 0x77 # fixed by manufacture.
        
        # read calibration data
        data = self.bus.read_i2c_block_data(self.addr, 0xAA, 22)
        
        raw = b''
        
        for n in range(11):
            raw += struct.pack('BB', data[n*2+1], data[n*2])
        
        [\
        self.AC1, self.AC2, self.AC3, \
        self.AC4, self.AC5, self.AC6, \
        self.B1,  self.B2, \
        self.MB,  self.MC,  self.MD] = struct.unpack("hhhHHHhhhhh", raw)
        return
    
    
    def reset(self):
        '''
        Reset sensor.
        
             by write soft reset command 0xB6 to reset register 0xE0.
        '''
        self.bus.write_byte_data(self.addr, 0xE0, 0xB6)
        return
        
    
    def check_communication(self):
        '''
        Communication check.
        
            return True if commuication is established, otherwise False.
        '''
        # always get 0x55 on well created links.
        return self.bus.read_byte_data(self.addr, 0xD0) == 0x55
        
        
    def read_temperature(self):
        '''
        Read sensor for temperature.
        
            return temperature in degree Celcius.
        '''
        self.bus.write_byte_data(self.addr, 0xF4, 0x2E)
 
        while self.bus.read_byte_data(self.addr, 0xF4) & 0x20:
            #print('Waiting for temperature data ...')
            continue
        
        raw_temp = self.bus.read_i2c_block_data(self.addr, 0xF6, 2)
        UT = struct.unpack('h', struct.pack('BB', raw_temp[1], raw_temp[0]))
        UT = UT[0]
                
        X1 = (UT - self.AC6) * self.AC5 / 2**15
        X2 = (self.MC * 2**11) / (X1 + self.MD)
        B5 = X1 + X2
        degree_Celsius = (B5 + 8) / 2**4 / 10
        return degree_Celsius
    
    
    def read_pressure(self, over_sampling):
        '''
        Read sensor for air pressure.
        
            return temperature in degree Celcius and pressure in Pa.
            
            over_sampling : 0x00 - 0x03
            larger over_sampling leads to more accuracy but longer sample time.
        '''
        t, p = self.read_TP(over_sampling)
        return p
    
    def read_TP(self, over_sampling):
        '''
        Read sensor for temperature and air pressure.
        
            return pressure in Pa.
        '''
        # get temperature        
        self.bus.write_byte_data(self.addr, 0xF4, 0x2E)
 
        while self.bus.read_byte_data(self.addr, 0xF4) & 0x20:
            #print('Waiting for temperature data ...')
            continue
        
        raw_temp = self.bus.read_i2c_block_data(self.addr, 0xF6, 2)
        UT = struct.unpack('h', struct.pack('BB', raw_temp[1], raw_temp[0]))
        UT = UT[0]
        
        X1 = (UT - self.AC6) * self.AC5 / 2**15
        X2 = (self.MC * 2**11)/(X1 + self.MD)
        B5 = X1 + X2
        degree_Celsius = (B5 + 8) / 2**4 /10
        
        #----------------------------------------------------------------------
        # get air pressure
        
        # pressure data processing depends on temperature parameter B5 upper,
        # so, a pressure reading should perform a pressure reading first.
        
        over_sampling = min(3, over_sampling)
        over_sampling = max(0, over_sampling)
        
        
        self.bus.write_byte_data(self.addr, 0xF4, 0x34 + (over_sampling<<6))
 
        while self.bus.read_byte_data(self.addr, 0xF4) & 0x20:
            #print('Waiting for pressure data ...')
            continue
        
        raw_pressure = self.bus.read_i2c_block_data(self.addr, 0xF6, 3)        
        UP = ((raw_pressure[0]<<16) + (raw_pressure[1]<<8) + raw_pressure[2])>>(8-over_sampling)
 
        B6 = B5 - 4000
        X1 = (self.B2 * (B6**2/2**12))/2**11
        X2 = self.AC2 * B6 / 2**11
        X3 = X1 + X2
 
        B3 = ((int(self.AC1 * 4 + X3) << over_sampling) + 2) / 4
        X1 = self.AC3 * B6 / 2**15 # ? 15 ?
        X2 = (self.B1 * (B6 ** 2 / 2 ** 12)) / 2**16
        X3 = ((X1 + X2) + 2) / 2**2
        
        B4 = self.AC4 * (X3 + 32768) / 2**15 # !!
        B7 = (UP - B3) * (50000 >> over_sampling)
        
        p = (B7 * 2 / B4) if B7 < 0x80000000 else B7 / B4 *2
        X1 = (p / 2**11) ** 2
        X1 = X1 * 3038 / 2**16
        X2 = (-7357 * p) / 2**16
        pascar = p + (X1 + X2 + 3791) / 2**4
        #----------------------------------------------------------------------
        return degree_Celsius, pascar
        
        
def test(i2c_interface_id, over_sampling):
    bmp180 = BMP180(i2c_interface_id)
 
    while True:
        t, p = bmp180.read_TP(over_sampling)
        t = str(t)[:4] + '℃'
        p = str(p/100)[:6] + 'x100Pa'
        print(t,p)
    
 
if __name__ == '__main__':
    test(1, 3)