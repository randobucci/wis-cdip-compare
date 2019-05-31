'''
* wis_aggregate.py
* WIS data are organized by month, this code will aggregate 
* Aggregate individual WIS netcdf files for entire year and plot
* https://chlthredds.erdc.dren.mil/thredds/catalog/wis/Atlantic/ST44098/2008/catalog.html
exec(open("wis_aggregate.py").read())
'''

#- Import libraries
import netCDF4
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mat_dates
from datetime import datetime
from dateutil.rrule import rrule, MONTHLY
import dateutil.parser
import time
import calendar

#- NDBC Station
ndbc_id = '44098' #- 160- jeffrey's Ledge
cdip_id = '163'
buoy_name = 'Jeffreys Ledge'
region = 'Atlantic'
start_date = '20080101'
end_date = '20081231'
end_date = '20080430'

#- Define a function to convert date_string (YYYYMMDD) to datetime obj 
def str_datetime(d):
    return (datetime.strptime(d,'%Y%m%d'))

#- convert to datetime objects
start_dt = str_datetime(start_date)
end_dt = str_datetime(end_date)


#- get a list of months between start and end time
dates = [dt for dt in rrule(MONTHLY, dtstart=start_dt,until=end_dt)]

#- Read in data from muli-file netCDF dataset.
#- Reference: https://unidata.github.io/netcdf4-python/netCDF4/index.html#section8
fnames = []
for dt in dates:
    year = dt.strftime('%Y')	#- '2008'
    month = dt.strftime('%m')	#- '02'
    wis_url = 'https://chlthredds.erdc.dren.mil/thredds/dodsC/wis/'+ \
          region+'/ST'+ndbc_id+'/'+year+'/'
    nc_file = 'WIS-ocean_waves_ST'+ndbc_id+'_'+year+month+'.nc'
    fnames.append(wis_url+nc_file)

#- Try using xarray library to merge mulitple netCDF files
DS = xr.open_mfdataset(fnames)

#- Use xarray.values to get values as numpy object
nc_time = DS.time.values

#- Function to convert numpy64 to datetime
#- https://gist.github.com/blaylockbk/1677b446bc741ee2db3e943ab7e4cabd
def to_datetime(date):
    """
    Converts a numpy datetime64 object to a python datetime object 
    Input:
      date - a np.datetime64 object
    Output:
      DATE - a python datetime object
    """
    timestamp = ((date - np.datetime64('1970-01-01T00:00:00'))
                 / np.timedelta64(1, 's'))
    return datetime.utcfromtimestamp(timestamp)

wave_time = [to_datetime(t) for t in nc_time]
Hs = DS.waveHs.values
Tp = DS.waveTp.values
Dp = DS.waveMeanDirection.values



# Function to find nearest value in numpy array
def find_nearest(array,value):
    idx = (np.abs(array-value)).argmin()
    return array[idx]

# Function to convert from human-format to UNIX timestamp
def get_timestamp(humanTime,dateFormat):
    unixTimestamp = int(time.mktime(datetime.strptime(humanTime, dateFormat).timetuple()))
    return unixTimestamp

'''
#- Get time indices: That is find the UNIX timestamp values that correspond to Start and End dates entered above
#- Note: this isn't important if small time-series, gets more important for large datasets
unix_start = get_timestamp(start_date,"%Y%m%d") 
nearest_start = find_nearest(nc_time, unix_start)  # Find the closest unix timestamp
start_index = np.where(nc_time==nearest_start)[0][0]  # Grab the index number of found date
unix_end = get_timestamp(end_date,"%Y%m%d")
future = find_nearest(nc_time, unix_end)  # Find the closest unix timestamp
end_index = np.where(nc_time==future)[0][0]  # Grab the index number of found date


'''
#- Plot wave bulk parameters 
# Create figure and specify subplot orientation (3 rows, 1 column), shared x-axis, and figure size
f, (pHs, pTp, pDp) = plt.subplots(3, 1, sharex=True, figsize=(15,10)) 

# Create 3 stacked subplots for three PARAMETERS (Hs, Tp, Dp)
pHs.plot(wave_time,Hs,'b')
pTp.plot(wave_time,Tp,'b')
pDp.scatter(wave_time,Dp,color='blue',s=5) # Plot Dp variable as a scatterplot, rather than line

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
months = mat_dates.MonthLocator(interval=1) 
daysFmt = mat_dates.DateFormatter('%m/%d')
plt.gca().xaxis.set_major_locator(months)
plt.gca().xaxis.set_major_formatter(daysFmt)

# Label x-axis
plt.xlabel('Month', fontsize=18)
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



