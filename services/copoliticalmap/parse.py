import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import geopandas as gpd
import base64
import datetime
import io
import numpy as np


filename = './co_counties_voters.geojson'
file=open(filename)
counties_gdf = gpd.read_file(file)
print(counties_gdf.columns)
print(counties_gdf.head(1))
print(counties_gdf['LABEL'])

df_cos = counties_gdf[['LABEL', 'CENT_LAT', 'CENT_LONG']]
print(df_cos)

df = pd.read_csv('./VotersByPartyStatus.csv')
df =df.fillna(value='0',axis=1)
for col in df.columns:
        if (col != 'County'):
#remove commas from numbers
            df[col] = df[col].astype(str)
            df[col] = df[col].str.replace(',','')
            df[col] = df[col].astype(float)
            df[col] = df[col].astype(np.int64)
print(df)

df_join = df.set_index('County').join(df_cos.set_index('LABEL'))
print(df_join)
print(df_join.shape)
print(df.columns)

df['DEM_total'] = df['DEM-Active'] + df['DEM-Inactive'] 
print(df['DEM_total'], df['DEM-Active'], df['DEM-Inactive'] )

df_dem = df[['DEM_total', 'DEM-Active', 'DEM-Inactive']]
print(df_dem)
