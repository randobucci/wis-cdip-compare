'''
* wis_test.py
* Will open WIS data and perform analysis
* https://chlthredds.erdc.dren.mil/thredds/catalog/wis/Atlantic/ST44098/2008/catalog.html
exec(open("wis_test.py").read())
'''

#- Import libraries
import netCDF4
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mat_dates
import datetime
import time
import calendar

#- NDBC Station
ndbc_id = '44098' #- 160- jeffrey's Ledge
cdip_id = '163'
buoy_name = 'Jeffreys Ledge'
region = 'Atlantic'
start_date = '20080901'
end_date = '20080930'
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
Dp = nc.variables['waveMeanDirection'] 


# Function to find nearest value in numpy array
def find_nearest(array,value):
    idx = (np.abs(array-value)).argmin()
    return array[idx]

# Function to convert from human-format to UNIX timestamp
def get_timestamp(humanTime,dateFormat):
    unixTimestamp = int(time.mktime(datetime.datetime.strptime(humanTime, dateFormat).timetuple()))
    return unixTimestamp


#- Get time indices: That is find the UNIX timestamp values that correspond to Start and End dates entered above
#- Note: this isn't important if small time-series, gets more important for large datasets
unix_start = get_timestamp(start_date,"%Y%m%d") 
nearest_start = find_nearest(nc_time, unix_start)  # Find the closest unix timestamp
start_index = np.where(nc_time==nearest_start)[0][0]  # Grab the index number of found date
unix_end = get_timestamp(end_date,"%Y%m%d")
future = find_nearest(nc_time, unix_end)  # Find the closest unix timestamp
end_index = np.where(nc_time==future)[0][0]  # Grab the index number of found date

#- Plot wave bulk parameters 
# Create figure and specify subplot orientation (3 rows, 1 column), shared x-axis, and figure size
f, (pHs, pTp, pDp) = plt.subplots(3, 1, sharex=True, figsize=(15,10)) 

# Create 3 stacked subplots for three PARAMETERS (Hs, Tp, Dp)
pHs.plot(wave_time[start_index:end_index],Hs[start_index:end_index],'b')
pTp.plot(wave_time[start_index:end_index],Tp[start_index:end_index],'b')
pDp.scatter(wave_time[start_index:end_index],Dp[start_index:end_index],color='blue',s=5) # Plot Dp variable as a scatterplot, rather than line

#- plot title
plot_title = nc.title+': STN '+ndbc_id+' ('+cdip_id+')'
# Set Titles
plt.suptitle(plot_title, fontsize=30, y=0.99)
plt.title(start_date + " - " + end_date, fontsize=20, y=3.45)

# Set tick parameters
pHs.set_xticklabels(['1','6','11','16','21','26','31']) 
pHs.tick_params(axis='y', which='major', labelsize=12, right='off')
pHs.tick_params(axis='x', which='major', labelsize=12, top='off')

# Set x-axis tick interval to every 5 days
days = mat_dates.DayLocator(interval=5) 
daysFmt = mat_dates.DateFormatter('%d')
plt.gca().xaxis.set_major_locator(days)
plt.gca().xaxis.set_major_formatter(daysFmt)

# Label x-axis
plt.xlabel('Day', fontsize=18)
# Make a second y-axis for the Hs plot, to show values in both meters and feet
pHs2 = pHs.twinx()

# Set y-axis limits for each plot
pHs.set_ylim(0,8)
pHs2.set_ylim(0,25)
pTp.set_ylim(0,28)
pDp.set_ylim(0,360)

# Label each y-axis
pHs.set_ylabel('Hs(m)', fontsize=18)
pHs2.set_ylabel('Hs(ft)', fontsize=18)
pTp.set_ylabel('Tp(s)', fontsize=18)
pDp.set_ylabel('Dmean(deg)', fontsize=18)

# Plot dashed gridlines
pHs.grid(b=True, which='major', color='b', linestyle='--')
pTp.grid(b=True, which='major', color='b', linestyle='--')
pDp.grid(b=True, which='major', color='b', linestyle='--')

plt.show()




