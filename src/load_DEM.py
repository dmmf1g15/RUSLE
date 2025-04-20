from RUSLE_functions import *
import rasterio
from rasterio.windows import Window
import geopandas as gpd
import matplotlib.pyplot as plt

def get_elevation(DEM_path,lat1,long1):
    #We need to convert to a the portugese crs
    df=pd.DataFrame({'lat':[lat1],'long':[long1]})
    gdf=gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.long, df.lat), crs='EPSG:4326')
    gdf_port=gdf.to_crs('EPSG:3763')
    lat_port=gdf_port.geometry.to_list()[0].x
    long_port=gdf_port.geometry.to_list()[0].y
    with rasterio.open(DEM_path) as DEM_file:
        meta=DEM_file.meta
        rowcol = rasterio.transform.rowcol(meta['transform'], xs=lat_port, ys=long_port)

        y = rowcol[0]
        x = rowcol[1]
        print((x,y))

        # Load specific pixel only using a window
        width=50
        height=50
        window = Window(x-width/2,y-height/2,width,height)
        arr = DEM_file.read(window=window)
    return arr[0],window



DEM_path='./data/dem_srtm_pt_25m.geotiff'

lat,long=37.289803, -8.858953
#37.327615, -8.725525
#39.102983, -8.758106
height_arr,window=get_elevation(DEM_path,lat, long)
import matplotlib.pyplot as plt
plt.figure()
plt.contour(np.flipud(height_arr),levels=20)
plt.figure()
plt.imshow(height_arr)
plt.show()