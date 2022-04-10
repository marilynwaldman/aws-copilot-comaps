import pandas as pd
import geopandas as gpd
import plotly.graph_objects as go
import numpy as np

def clean_data(df, counties_gdf):
    print('cleaning data')

# fill missing with 0
    df =df.fillna(value='0',axis=1)

    for col in df.columns:
        if (col != 'County'):
#remove commas from numbers
            df[col] = df[col].astype(str)
            df[col] = df[col].str.replace(',','')
            df[col] = df[col].astype(float)
            df[col] = df[col].astype(np.int64)

    for i in range(len(counties_gdf)):
        df.at[i,'%Active']=100.*df.at[i,'Total-Active']/df.at[i,'Total']

#now updating df
    counties_gdf['Republicans']=0
    counties_gdf['Democrats']=0
    counties_gdf['Unaffiliated']=0
    counties_gdf['Max']=None
    counties_gdf['Total']=0


#    figure.update_traces(locations=counties_gdf,selector=dict(type='choropleth'))
#    figure.add_trace(go.Scatter,data=counties_gdf)

    partial = 0.75

    for c in counties_gdf['LABEL']:
        county_index = counties_gdf[counties_gdf['LABEL']==c].index[0]
        #print('LABEL',county_index)
        voter_index = df[df['County']==c].index[0]
        #print('Voter',voter_index)
        gop_total = df.at[voter_index,'REP-Active']+df.at[voter_index,'REP-Inactive']
        counties_gdf.at[county_index,'Republicans'] = gop_total
        dem_total = df.at[voter_index,'DEM-Active']+df.at[voter_index,'DEM-Inactive']
        counties_gdf.at[county_index,'Democrats'] = dem_total
        uaf_total = df.at[voter_index,'UAF-Active']+df.at[voter_index,'UAF-Inactive']
        counties_gdf.at[county_index,'Unaffiliated'] = uaf_total
        counties_gdf.at[county_index,'Total']=(gop_total + dem_total + uaf_total)/1000.

        if ((counties_gdf.at[county_index,'Unaffiliated'] > counties_gdf.at[county_index,'Democrats']) and \
            (counties_gdf.at[county_index,'Unaffiliated'] > counties_gdf.at[county_index,'Republicans'])):
            if (counties_gdf.at[county_index,'Democrats']/counties_gdf.at[county_index,'Unaffiliated'] > partial):
                counties_gdf.at[county_index,'Max']=1
            elif (counties_gdf.at[county_index,'Republicans']/counties_gdf.at[county_index,'Unaffiliated'] > partial):
                counties_gdf.at[county_index,'Max']=3
            else:
                counties_gdf.at[county_index,'Max']= 2
        elif ((counties_gdf.at[county_index,'Republicans'] > counties_gdf.at[county_index,'Democrats']) and \
            (counties_gdf.at[county_index,'Republicans'] > counties_gdf.at[county_index,'Unaffiliated'])):
            counties_gdf.at[county_index,'Max']= 4  
        elif ((counties_gdf.at[county_index,'Democrats'] > counties_gdf.at[county_index,'Unaffiliated']) and \
            (counties_gdf.at[county_index,'Democrats'] > counties_gdf.at[county_index,'Republicans'])):
            counties_gdf.at[county_index,'Max']= 0
        else:
            print('Error, no max found')
            exit()

    print(counties_gdf.columns)
    print("counties_gdf")
    print(counties_gdf.head(2))


    return counties_gdf


def get_map_attributes(counties_gdf):
    # prepare data for plot
    lats = counties_gdf['CENT_LAT']
    lons = counties_gdf['CENT_LONG']
    sizes = counties_gdf['Total']
    for i in range(0,len(sizes)):
        sizes[i] = sizes[i].astype(int).item()
        sizes[i] = min(sizes[i],150) 
        sizes[i] = max(10,sizes[i])
        #print('s=',sizes[i])
        #print(type(sizes[i]))

    colors = []
    color_key = ["blue","lightblue","grey","pink","red"]
    for i in range(0,len(counties_gdf['Max'])):
        m = int(counties_gdf['Max'][i])
        #print('i=',i,' m=',m,color_key[m])
        colors.append(color_key[m])

    labels = []
    reps = counties_gdf['Republicans'].astype(int).astype(str)
    uafs = counties_gdf['Unaffiliated'].astype(int).astype(str)
    dems = counties_gdf['Democrats'].astype(int).astype(str)
    for i in range(0,len(counties_gdf['LABEL'])):
        labels.append(counties_gdf['LABEL'][i] + '\nRep: '+reps[i] + '\nUAF: '+uafs[i]+'\nDems: '+dems[i])

    print('lat',type(lats),'lon',type(lons))  
    lats = lats.tolist()
    print(lats[0])
    lons = lons.tolist()
    print(lons[0])
    sizes = sizes.tolist()
    print(sizes[0])
    print(labels[0])
    print(colors[0])
    return lats, lons, labels, sizes, colors 
