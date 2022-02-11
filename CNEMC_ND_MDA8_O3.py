# deseasonlize and normalize the summertime MDA8O3 from 2014 to 2021 in BTH, YRD and PRD regions

import numpy as np
from netCDF4 import Dataset

def moving_avg(data):
    
    data_avg = np.zeros((92))
    for m in range(0,len(data)-21):
        data_avg[m] = data[m+21]-np.nanmean(data[m:m+21])
    return data_avg

def main():
    
    file_o3 = '/home/lss/data/O3_meteo/data_extract/vc_sta_std/CNEMC/CNEMC_MDA8_O3.nc'
    dataset = Dataset(file_o3)
    o3_bth = dataset.variables['O3_bth'][:]
    o3_yrd = dataset.variables['O3_yrd'][:]
    o3_prd = dataset.variables['O3_prd'][:]
    dataset.close()
    O3 = np.append(o3_bth,o3_yrd,axis=1)
    O3 = np.append(O3,o3_prd,axis=1)
    
    O3_avg = np.zeros((8,len(O3[0]),92))
    O3_de = np.zeros((8,len(O3[0]),92))
    for j in range(0,len(O3[0])):
        for i in range(0,len(O3)):
            O3_avg[i,j,:] = moving_avg(O3[i,j,:])
        O3_de[0:4,j] = O3_avg[0:4,j]/np.nanstd(O3_avg[0:4,j])
        index = np.where(O3_de[0:4,j]>np.nanpercentile(O3_de[0:4,j],90))
        O3_de[4:,j] = O3_avg[4:,j]/np.nanstd(O3_avg[4:,j])
        index = np.where(O3_de[4:,j]>np.nanpercentile(O3_de[4:,j],90))
    
    file_output = '/home/lss/data/O3_meteo/data_extract/vc_sta_std/CNEMC/CNEMC_ND_MDA8_O3.nc'
    f_w = Dataset(file_output,'w',format='NETCDF4')
    f_w.createDimension('year',8)
    f_w.createDimension('days',92)
    f_w.createDimension('BTH',len(o3_bth[0]))
    f_w.createDimension('YRD',len(o3_yrd[0]))
    f_w.createDimension('PRD',len(o3_prd[0]))
    f_w.createVariable('O3_bth',np.float32,('year','BTH','days'))
    f_w.createVariable('O3_yrd',np.float32,('year','YRD','days'))
    f_w.createVariable('O3_prd',np.float32,('year','PRD','days'))
    f_w.variables['O3_bth'][:] = O3_de[:,0:len(o3_bth[0]),:]
    f_w.variables['O3_yrd'][:] = O3_de[:,len(o3_bth[0]):len(o3_bth[0])+len(o3_yrd[0]),:]
    f_w.variables['O3_prd'][:] = O3_de[:,len(o3_bth[0])+len(o3_yrd[0]):len(o3_bth[0])+len(o3_yrd[0])+len(o3_prd[0]),:]
    f_w.close()  

if __name__=='__main__':
    main()
