import xarray as xr
import geopandas as gpd
import pandas as pd
import os

# Reading the nc files with the xarray library
tmed_nc = xr.open_dataset(
    'T_ave.nc')

tmax_nc = xr.open_dataset(
    r'T_max.nc')

tmin_nc = xr.open_dataset(
    r'T_min.nc')

tsoil_nc = xr.open_dataset(
    r'T_soil.nc')

precip_nc = xr.open_dataset(
    r'Precip.nc')

# Finding the multi annual mean value for every grid for the temperature variables
tmed = tmed_nc.tmed.mean(dim='Time')
tmax = tmax_nc.tmax.mean(dim='Time')
tmin = tmin_nc.tmin.mean(dim='Time')
tsoil = tsoil_nc.tsoil.mean(dim='Time')

# Finding the multi annual mean value for every grid for the precipitation variable
precip = (precip_nc
          .groupby('Time.year')
          .sum(dim='Time', skipna=True)
          .mean(dim='year'))
precip = precip.where(precip != 0)

# Converting the .nc to dataframe
tmed_df = (tmed.to_dataframe()
           .dropna()
           .reset_index())

tmax_df = (tmax.to_dataframe()
           .dropna()
           .reset_index())

tmin_df = (tmin.to_dataframe()
           .dropna()
           .reset_index())

tsoil_df = (tsoil.to_dataframe()
            .dropna()
            .reset_index())

precip_df = (precip.to_dataframe()
             .dropna()
             .reset_index())

# Saving the dataframes as csv
tmed_df.to_csv('tmed_df_romania.csv', index=False)
tmax_df.to_csv('tmax_df_romania.csv', index=False)
tmin_df.to_csv('tmin_df_romania.csv', index=False)
tsoil_df.to_csv('tsoil_df_romania.csv', index=False)
precip_df.to_csv('precip_df_romania.csv', index=False)

# Saving the dataframes as .shp
for file in os.listdir():
    if file.endswith('.csv'):
        points_df = pd.read_csv(file)
        x = points_df.Longitude
        y = points_df.Latitude
        points_df['geometry'] = gpd.points_from_xy(x, y)
        points_shp = gpd.GeoDataFrame(points_df, geometry='geometry', crs='EPSG:4326')
        points_shp.to_file(f'shapefile/{file[:-4]}.shp', crs='EPSG:4326')

# Saving as tif
(tmed
 .rio
 .set_spatial_dims('Longitude',
                   'Latitude')
 .rio
 .write_crs("epsg:4326")
 .rio
 .to_raster('tif/tmed.tif'))

(tmax
 .rio
 .set_spatial_dims('Longitude',
                   'Latitude')
 .rio
 .write_crs("epsg:4326")
 .rio
 .to_raster('tif/tmax.tif'))

(tmin
 .rio
 .set_spatial_dims('Longitude',
                   'Latitude')
 .rio
 .write_crs("epsg:4326")
 .rio
 .to_raster('tif/tmin.tif'))

(tsoil
 .rio
 .set_spatial_dims('Longitude',
                   'Latitude')
 .rio
 .write_crs("epsg:4326")
 .rio
 .to_raster('tif/tsoil.tif'))

(precip
 .rio
 .set_spatial_dims('Longitude',
                   'Latitude')
 .rio
 .write_crs("epsg:4326")
 .rio
 .to_raster('tif/precip.tif'))
