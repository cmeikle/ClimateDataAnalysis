import xarray as xr
#import cartopy.crs as ccrs
import matplotlib.pyplot as plt

# open dataset using xarray downloaded from https://www.temis.nl/airpollution/absaai/
data_file = "../data/ESACCI-AEROSOL-L3-AAI-GOME2A-1D-20210813-fv1.8.nc"
DS = xr.open_dataset(data_file)

# Choose the absording aerosol index info from DataSet and load into DataArray
da = DS.absorbing_aerosol_index

if __name__ == "__main__":
    print(da.shape)
    #da = da.values
    # Draw coastlines of the Earth
    #ax = plt.axes()#projection=ccrs.PlateCarree())
    #ax.coastlines()
    # Output a contour plot of the information
    da.plot.contour()
    plt.xlabel('Latitude')
    plt.ylabel('Longitude')
    plt.title('Aerosol index 13th Aug 2021')
    plt.savefig("../img/Aerosol index 13th Aug 2021.png")
    plt.show()
