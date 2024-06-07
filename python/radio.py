import machine
from machine import Pin
import time
import math
import si5351

class Radio:
    MIN_AM_FREQUENCY = const( 400000 )
    MAX_AM_FREQUENCY = const( 4000000 )
    MIN_HAM_FREQUENCY = const( 4000000 ) # buffer for 2MHz
    MAX_HAM_FREQUENCY = const( 32000000 )
    
# 	MIN_RADIX = const( 0 )
# 	MAX_RADIX = const( 6 )
# 	
# 	MODE_FREQUENCY = const( 1 )
# 	MODE_RADIX = const( 2 )
# 	
# 	STARTING_RADIX = const(2)
    
    def __init__(self, s, frequency, band):
        self._si5351 = s
        self._frequency = frequency
        self._frequency_AM = 10700000-frequency if frequency < 10700000 else frequency-10700000
        self._frequency_mixer = frequency
        self._band = band+1 if band < 3 else band-1 # 0 AM (.5-1.7), 1 LOW (5-16), 2 HIGH (16-30), 3 Bypass
        self._new_band = band
        self._band_is_auto = True
        self._mult = 100
        self._old_mult = 0
        self._mult_AM = 80
        self._am_AM = False
        self._si5351.clock_0.drive_strength( si5351.STRENGTH_2MA )
        self._si5351.clock_1.drive_strength( si5351.STRENGTH_2MA )
        self._si5351.clock_2.drive_strength( si5351.STRENGTH_2MA )
        
        self._bpf_s0 = Pin(27, Pin.OUT)
        self._bpf_s1 = Pin(26, Pin.OUT)
        

    def setBPF(self):
        f = self._frequency_mixer
        
        # check if proper frequency
        if f < MIN_AM_FREQUENCY:
            raise Exception("frequency too low")
        elif f > MAX_HAM_FREQUENCY:
            raise Exception("frequency too high")
        elif f > MAX_AM_FREQUENCY and f < MIN_HAM_FREQUENCY:
            raise Exception("frequency between AM and HAM")
        
        # figure out Bypass and manual BPF logic
        if self._band_is_auto: # auto BPF
            if f < 16000000 and f >= MIN_HAM_FREQUENCY and self._band != 1: # LOW
                self._band = 1
                self._bpf_s0.value(1)
                self._bpf_s1.value(0)
            elif f >= 16000000 and self._band != 2: # HIGH
                self._band = 2
                self._bpf_s0.value(0)
                self._bpf_s1.value(1)
            elif f < MAX_AM_FREQUENCY and self._band != 0: # AM
                self._band = 0
                self._bpf_s0.value(0)
                self._bpf_s1.value(0)
                self._frequency_AM = 10700000 - self._frequency
                self._frequency_mixer = 10700000
        elif self._new_band < 0 or self._new_band > 3:
            self._new_band = self._band
            raise Exception("Invalid band")
        elif self._new_band != self._band: # manual BPF
            self._band = self._new_band
            if self._band == 1: # LOW
                self._bpf_s0.value(1)
                self._bpf_s1.value(0)
            elif self._band == 2: # HIGH
                self._bpf_s0.value(0)
                self._bpf_s1.value(1)
            elif self._band == 0: # AM
                self._bpf_s0.value(0)
                self._bpf_s1.value(0)
                self._frequency_AM = 10700000 - self._frequency
                self._frequency_mixer = 10700000
            else: # Bypass
                self._bpf_s0.value(1)
                self._bpf_s1.value(1)
                self._mixer_frequency = self._frequency
                
        # Update AM frequency
        if self._band == 0:
            self._am_AM = True
            self._frequency_AM = 10700000 - self._frequency
            self._frequency_mixer = 10700000
        else:
            self._frequency_AM = 0

    def setFrequency(self):
        # set BPF and check frequency range
        self.setBPF()
        
        f = self._frequency_mixer
        f_AM = self._frequency_AM  
        
        # set mixer frequency
        if f < 5000000:
            self._mult = 110
        elif f < 8000000:
            self._mult = 100
        elif f < 11000000:
            self._mult = 80
        elif f < 15000000:
            self._mult = 50
        else:
            self._mult = 30
            
        #print(f)
        #print(f_AM)
        #print(self._mult)
         

        if (not self._frequency_AM) and self._am_AM:
            self._am_AM = False
            self._si5351 = si5351.SI5351( data=Pin(4), clock=Pin(5), addr=0x60 ) # reinitialize

        self._si5351.set_frequency( self._frequency_mixer, self._si5351.clock_0, self._si5351.pll_a, self._mult )
        self._si5351.set_frequency( self._frequency_mixer, self._si5351.clock_1, self._si5351.pll_a, self._mult )
        
        if ( self._mult != self._old_mult ):
            self._si5351.set_phase( self._si5351.clock_1, self._si5351.pll_a, self._mult )
        self._old_mult = self._mult
        
        if self._frequency_AM: # requires slight modification to si5351.py
            self._si5351.outputs_enabled = 0x00 # 0xff -- enable all
            if f_AM < 8000000:
                self._mult_AM = 100
            elif f_AM < 11000000:
                self._mult_AM = 80
            elif f_AM < 15000000:
                self._mult_AM = 50
            else:
                self._mult_AM = 30
            
            self._si5351.set_frequency( self._frequency_AM, self._si5351.clock_2, self._si5351.pll_b, self._mult_AM )
        else:
            self._si5351.outputs_enabled = 0X04 # disable clk2
        
        
    def run(self):
        #print(self._frequency)
        self.setFrequency()
        self._band_is_auto = True
        while True:
            user_input = input()
            if user_input == "FREQ,":
                print(self._frequency)
                #print(self._frequency_AM)
                #self.setFrequency()
                print("OK")
            elif user_input.startswith("FREQ,"):
                try:
                    self._frequency = int(user_input[5:13])
                    self._frequency_mixer = self._frequency
                    print(self._frequency)
                    self.setFrequency()
                    print("OK")
                except:
                    print("Error: Invalid frequency")
            elif user_input == "BAND,":
                print(self._band)
                print("OK")
            elif user_input == "BAND,AUTO":
                self._band_is_auto = True
                self.setBPF()
                print(self._band)
                print("OK")
            elif user_input.startswith("BAND,"):
                try:
                    self._new_band = int(user_input[5])
                    self._band_is_auto = False
                    self.setBPF()
                    print(self._band)
                    print("OK")
                except:
                    print("Error: Invalid band")
            elif user_input.startswith("VER"):
                print("SDR Pi Pico version 0.1")
                print("OK")
            elif user_input == "EXIT":
                break
            time.sleep(0.05)

