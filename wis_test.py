'''
* wis_test.py
* Will open WIS data and perform analysis
* https://chlthredds.erdc.dren.mil/thredds/catalog/wis/Atlantic/ST44098/2008/catalog.html
'''

#- Import libraries
import netCDF4
import numpy as np
import matplotlib.pyplot as plt
import datetime
import time
import calendar

#- NDBC Station
ndbc_id = '44098' #- 160- jeffrey's Ledge
region = 'Atlantic'
start_date = '20080901'
end_date = '20121231'
year = start_date[0:4]
month = start_date[4:6]
day=start_date[6:8]

#- Access WIS data
#- OPeNDAP access:
#- https://chlthredds.erdc.dren.mil/thredds/dodsC/wis/Atlantic/ST44098/2008/WIS-ocean_waves_ST44098_200812.nc
#- Direct File Access:
#- 'https://chlthredds.erdc.dren.mil/thredds/fileServer/wis/Atlantic/ST44098/2008/WIS-ocean_waves_ST44098_200812.nc'
wis_url = 'https://chlthredds.erdc.dren.mil/thredds/dodsC/wis/'+ \
          region+'/ST'+ndbc_id+'/'+year+'/'
nc_file = 'WIS-ocean_waves_ST'+ndbc_id+'_'+year+month+'.nc'
nc = netCDF4.Dataset(wis_url+nc_file)

#- Get list of variable names
wis_vars = nc.variables.keys()

#- Grab times and convert to array of datetime objects
nc_time = nc.variables['time'][:] 	# seconds since 1970-01-01 00:00:00 UTC
wave_time = [datetime.datetime.fromtimestamp(t) for t in nc_time]

Hs = nc.variables['waveHs']
Tp = nc.variables['waveTp']
Dp = nc.variables['waveDirection'] 


# Function to find nearest value in numpy array
def find_nearest(array,value):
    idx = (np.abs(array-value)).argmin()
    return array[idx]



