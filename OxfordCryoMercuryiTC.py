# -*- coding: utf-8 -*-
"""
Created on Thu Aug 30 18:36:18 2018

@author: ovj

%reset does magic
"""


import numpy as np
import pandas as pd
import time #for time delay function time.sleep
import visa
import matplotlib.pyplot as plt


#%%
# =============================================================================
# Define Functions
# =============================================================================

def autoPIDtoTemp(targetT=300):
    if 1<targetT<510:
        tset = str(targetT) # Units = K
        inst.query('SET:DEV:MB1.T1:TEMP:LOOP:TSET:%s' %tset)
        inst.query('SET:DEV:MB1.T1:TEMP:LOOP:ENAB:ON')
    else:
        print("Temperatrure out of Range")


def readTemp():
    currTemp = float(inst.query('READ:DEV:MB1.T1:TEMP:SIG:TEMP').split("TEMP:")[-1].strip()[:-1])
    
    return currTemp

def PIDHeatOff():
    inst.query('SET:DEV:MB1.T1:TEMP:LOOP:ENAB:OFF')
    inst.query('SET:DEV:MB1.T1:TEMP:LOOP:HSET:0') 


def readTempSim():    # needed for debugging
    return np.random.uniform(300,320)


def Cel2K(CelDeg):
    return CelDeg + 273.15


'''
#==============================================================================
# Do stuff from here ....
#==============================================================================
'''
#%% 
#==============================================================================
# Connect to instrument
#==============================================================================

rm = visa.ResourceManager()
inst = rm.open_resource('COM6')    # COM-Port may vary - check in device manager
inst.query('*IDN?')   # Check connection successful. MercuryiCT needs a driver (can be downloaded from Oxford) to make Serial Port via USB work!



#%%  
#==============================================================================
# Read current temperature
#==============================================================================

readTemp()

#%%
#==============================================================================
# Tell MercuryiCT to go to temperature 1<T<510 [K]
#==============================================================================
      
autoPIDtoTemp(315)

#%%
#==============================================================================
# Turn heater off - safe state.
#==============================================================================

PIDHeatOff()

#%%
#==============================================================================
# Read Temperature over time
#==============================================================================

NSamples = 10 
interval = 1 #in seconds


data=pd.DataFrame(index=np.arange(0,NSamples),columns=["Time [s]","Temp [K]"])
for i in range(NSamples):
    data.iloc[i] = [time.time(),round(readTempSim(),3)]
#    read = pd.DataFrame([time.time(),readTempSim()], columns=["Time","Temp"])    
#    temp.append(read.transpose(), ignore_index=True)
    time.sleep(interval)
    print("T="+str(data.loc[i]["Temp [K]"]))

#%%
#==============================================================================
# Plot Temperature 
#==============================================================================

fig1 = plt.figure("Mercury iCT - Temperature v. Time")
ax1 = fig1.add_subplot(111)
ax1.set_title("Temperature")
ax1.set_xlabel("Time [s]")
ax1.set_ylabel("Temperature [K]")

ax1.plot(data["Time [s]"]-data["Time [s]"][0],data["Temp [K]"], 'bo')

#%%
#==============================================================================
# Temperature Sweep
#==============================================================================


listTemp = [305,310,315,320] #Celsius

waitMinAtT= 3 # Minutes  

tmax = 120*60         
startTime = time.time()
for Temp in listTemp:
    autoPIDtoTemp(Temp)
    t=0
    while abs(readTemp()-Temp) > 0.5:
        print(readTemp())
        time.sleep(1)
        t +=1
        if t > tmax:
            break
        
    TempReached=time.time()
    while time.time()-TempReached < waitMinAtT*60:
        print(readTemp())
        time.sleep(1)

PIDHeatOff()

    

'''
#==============================================================================
# ... to here.
#==============================================================================
'''


#%%

''' 
Individual Commands below. Mark and unquot (ctrl+1)

'''

#
#
##%%
## =============================================================================
## Read Temperature
## =============================================================================
#inst.query('READ:DEV:MB1.T1:TEMP:SIG:TEMP')
#
#
##%%
##==============================================================================
## Set PID Target Temperature
##==============================================================================
#
#tset = str(305) # Units = K
#inst.query('SET:DEV:MB1.T1:TEMP:LOOP:TSET:%s' %tset)
#
#
##%%
## =============================================================================
## Turn PID-Control On
## =============================================================================
#inst.query('SET:DEV:MB1.T1:TEMP:LOOP:ENAB:ON')
#
#
##%%
## =============================================================================
## Set Heater to Percent
## =============================================================================
#hPer = str(0) # Units = Percent Power
#inst.query('SET:DEV:MB1.T1:TEMP:LOOP:HSET:%s' % hPer)
#
#
##%%
## =============================================================================
## Turn PID-Control Off - not reall needed
## =============================================================================
#inst.query('SET:DEV:MB1.T1:TEMP:LOOP:ENAB:OFF')
#inst.query('SET:DEV:MB1.T1:TEMP:LOOP:HSET:0') 
#
##%%
##==============================================================================
## Close connection to instrument to allow other programms to connect to it
##==============================================================================
#inst.close()


#%%

#==============================================================================
# To Do: MultiThreading
#==============================================================================
#!/usr/bin/python

#import thread
#import time
#
## Define a function for the thread
#def print_time( threadName, delay):
#   count = 0
#   while count < 5:
#      time.sleep(delay)
#      count += 1
#      print "%s: %s" % ( threadName, time.ctime(time.time()) )
#
## Create two threads as follows
#try:
#   thread.start_new_thread( print_time, ("Thread-1", 2, ) )
#   thread.start_new_thread( print_time, ("Thread-2", 4, ) )
#except:
#   print "Error: unable to start thread"
#
#while 1:
#   pass