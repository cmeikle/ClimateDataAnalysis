"""
Experimenting further with using xarray to downlad and analyse absorbing aerosol index datasets from 
https://www.temis.nl/airpollution/absaai/
"""
import xarray as xr
import matplotlib.pyplot as plt
import requests

from calendar import monthrange

def int_to_str(integer:int):
    int_as_str = str(integer)
    if len(int_as_str) == 1:
        return f"0{int_as_str}"
    else:
        return int_as_str

def aai_data(satellite:str, year:int, month:int, day:int):
    """
    A function for pulling down a particular date from data found at this address https://www.temis.nl/airpollution/absaai/,
    denoting the absorbing aerosol index at different points in the earths atmosphere
    """
    day = int_to_str(day)
    month = int_to_str(month)
    year = int_to_str(year)
    date = "".join([year, month, day])
    url = f"https://d1qb6yzwaaq4he.cloudfront.net/airpollution/absaai/{satellite}/daily/data/{year}/ESACCI-AEROSOL-L3-AAI-{satellite}-1D-{date}-fv1.8.nc"
    # request data from the url
    r = requests.get(url)
    filename = f"../data/aai_{date}.nc"
    with open(filename, "wb") as f:
        f.write(r.content)
    DS = xr.open_dataset(filename)
    # TODO: now that data has been loaded into memory could remove the file using the shutil package
     # Or possibly checking that the file is in memory instead of calling to url every time
    # Choose the absording aerosol index info from DataSet and load into DataArray
    da = DS.absorbing_aerosol_index.fillna(0)
    # remove values less than 0
    da = da.where(da > 0, 0)
    return da

def month_image(satellite, year, month):
    """
    Return an array for the mean monthly image
    """
    num_days = monthrange(year, month)[1]
    for day in range(1, num_days+1):
        # I don't really like this code, setting a variable inside a for loop, will want to tidy up in future
        if day == 1:
            da = aai_data(satellite, year, month, day)
        else:
            da += aai_data(satellite, year, month, day)
    da = da / num_days

    return da


if __name__ == "__main__":
    print(aai_data("GOME2A", 2021, 4, 24))
    da = month_image("GOME2A", 2021, 6)
    da.plot.contourf()
    plt.xlabel('Latitude')
    plt.ylabel('Longitude')
    plt.title('AAI June Monthly Mean image')
    plt.savefig("../img/AAI June Monthly Mean image.png")
    plt.show()

"""
Note: I would need to investigate and learn more about the dataset, why I am getting negative numbers and whether 
they should be removed as faulty data for some regions, white noise? 
However there is some resemlance in this mean image to the results produced at
https://d1qb6yzwaaq4he.cloudfront.net/airpollution/absaai/GOME2A/monthly/images/2021/GOME-2A_AAI_map_202106.png.
"""
    
    
