



from mercuryitc import MercuryITC
address = 'COM6'
m = MercuryITC(address)

help(serial)

print(m.serl)

print(m.modules)

htr = m.modules[0]
print(htr.nick)
htr.nick = 'Main Heater'
print(htr.nick)

print(htr.volt)

htr.volt = (2.5, 'V')
print(htr.volt)



#%%

import numpy as np
import os
import ctypes  # An included library with Python install.
import win32com.client #python activex client
import time #for time delay function time.sleep
import visa
import re
import serial
import matplotlib.pyplot as plt

rm = visa.ResourceManager()
inst = rm.open_resource('COM6')


inst.query('*IDN?')



#%%
# =============================================================================
# Set PID Target Temp
# =============================================================================

def autoPIDtoTemp(targetT=300):
    if 1<targetT<510:
        tset = str(targetT) # Units = K
        inst.query('SET:DEV:MB1.T1:TEMP:LOOP:TSET:%s' %tset)
        inst.query('SET:DEV:MB1.T1:TEMP:LOOP:ENAB:ON')
    else:
        print("Temperatrure out of Range")


def readTemp():
    currTemp = inst.query('READ:DEV:MB1.T1:TEMP:SIG:TEMP').split("TEMP:")[-1].strip()
    return currTemp

def PIDHeatOff():
    inst.query('SET:DEV:MB1.T1:TEMP:LOOP:ENAB:OFF')
    inst.query('SET:DEV:MB1.T1:TEMP:LOOP:HSET:0') 

        
autoPIDtoTemp(315)
PIDHeatOff()
readTemp()

temp=[]
duration = 10 #in seconds

for i in range(duration):
    temp.append([time.time(),readTemp()])
    time.sleep(1)
    print(temp[-1])


plt.plot(temp[)




#%%
# =============================================================================
# Read Temperature
# =============================================================================
inst.query('READ:DEV:MB1.T1:TEMP:SIG:TEMP')




#%%

tset = str(305) # Units = K
inst.query('SET:DEV:MB1.T1:TEMP:LOOP:TSET:%s' %tset)


#%%
# =============================================================================
# Turn PID-Control On
# =============================================================================
inst.query('SET:DEV:MB1.T1:TEMP:LOOP:ENAB:ON')


#%%
# =============================================================================
# Set Heater to Percent
# =============================================================================
inst.query('SET:DEV:MB1.T1:TEMP:LOOP:HSET:0')


#%%
# =============================================================================
# Turn PID-Control Off - not reall needed
# =============================================================================
inst.query('SET:DEV:MB1.T1:TEMP:LOOP:ENAB:OFF')
inst.query('SET:DEV:MB1.T1:TEMP:LOOP:HSET:0') 

#%%
inst.close()
