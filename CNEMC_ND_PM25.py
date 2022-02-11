# deseasonlize and normalize the wintertime daily mean PM2.5 from 2014 to 2021 in BTH, YRD and PRD regions

import numpy as np
from netCDF4 import Dataset

def moving_avg(data):
    
    data_avg = np.zeros((91))
    for m in range(0,len(data)-21):
        data_avg[m] = data[m+21]-np.nanmean(data[m:m+21])
    return data_avg

def main():
    
    file_pm = '/home/lss/data/O3_meteo/PM_process/vc_sta_std/CNEMC/CNEMC_PM25.nc'
    dataset = Dataset(file_pm)
    pm_bth = dataset.variables['PM_bth'][:]
    pm_yrd = dataset.variables['PM_yrd'][:]
    pm_prd = dataset.variables['PM_prd'][:]
    dataset.close()
    PM = np.append(pm_bth,pm_yrd,axis=1)
    PM = np.append(PM,pm_prd,axis=1)
    
    PM_avg = np.zeros((7,len(PM[0]),91))
    PM_de = np.zeros((7,len(PM[0]),91))
    for j in range(0,len(PM[0])):
        for i in range(0,len(PM)):
            PM_avg[i,j,:] = moving_avg(PM[i,j,:])
        PM_de[0:4,j] = PM_avg[0:4,j]/np.nanstd(PM_avg[0:4,j])
        index = np.where(PM_de[0:4,j]>np.nanpercentile(PM_de[0:4,j],90))
        PM_de[4:,j] = PM_avg[4:,j]/np.nanstd(PM_avg[4:,j])
        index = np.where(PM_de[4:,j]>np.nanpercentile(PM_de[4:,j],90))
    
    file_output = '/home/lss/data/O3_meteo/PM_process/vc_sta_std/CNEMC/CNEMC_ND_PM25.nc'
    f_w = Dataset(file_output,'w',format='NETCDF4')
    f_w.createDimension('year',7)
    f_w.createDimension('days',91)
    f_w.createDimension('BTH',len(pm_bth[0]))
    f_w.createDimension('YRD',len(pm_yrd[0]))
    f_w.createDimension('PRD',len(pm_prd[0]))
    f_w.createVariable('PM_bth',np.float32,('year','BTH','days'))
    f_w.createVariable('PM_yrd',np.float32,('year','YRD','days'))
    f_w.createVariable('PM_prd',np.float32,('year','PRD','days'))
    f_w.variables['PM_bth'][:] = PM_de[:,0:len(pm_bth[0]),:]
    f_w.variables['PM_yrd'][:] = PM_de[:,len(pm_bth[0]):len(pm_bth[0])+len(pm_yrd[0]),:]
    f_w.variables['PM_prd'][:] = PM_de[:,len(pm_bth[0])+len(pm_yrd[0]):len(pm_bth[0])+len(pm_yrd[0])+len(pm_prd[0]),:]
    f_w.close()  

if __name__=='__main__':
    main()
