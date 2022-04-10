import pandas as pd
import geopandas as gpd
import plotly.graph_objects as go
import numpy as np

def transform_df(df):
    # fill missing with 0
    df =df.fillna(value='0',axis=1)

    #remove commas from numbers and create np floats for all columns except County Name
    for col in df.columns:
        if (col != 'County'):
            df[col] = df[col].astype(str)
            df[col] = df[col].str.replace(',','')
            df[col] = df[col].astype(float)
            df[col] = df[col].astype(np.int64)

    df['Active'] = df['Total-Active'] * 100.0/ df['Total']

    return df  

def get_totals(df):
    # initialize party totals columns
    df['Republicans']=0
    df['Democrats']=0
    df['Unaffiliated']=0
    df['Max']= None
    df['Total']=0

    #compute sums
    df['Republicans'] = df['REP-Active'] + df['REP-Inactive']
    df['Democrats'] = df['DEM-Active'] + df['DEM-Inactive']
    df['Unaffiliated'] = df['UAF-Active'] + df['UAF-Inactive']
    df['Total'] = df['Unaffiliated'] + df['Democrats'] + df['Republicans'] 

    return df  

def join_geocoordinates(df, geodf):

    #df_join = df.set_index('County').join(geodf.set_index('LABEL'))
    df_join = pd.merge(df, geodf, left_on='County', right_on='LABEL') 
    return df_join



def find_max(df):     
    df['maxPartyValue'] = df[['Republicans', 'Democrats', 'Unaffiliated']].max(axis = 1)
    df['maxParty'] = df[['Republicans', 'Democrats', 'Unaffiliated']].idxmax(axis = 1)  
    df_temp = df[['Republicans', 'Democrats', 'Unaffiliated', 'Republicans', 'Democrats', 'Unaffiliated','maxPartyValue' ]]
    
    partial = .75
    df.loc[df.maxParty == 'Republicans', "Max"] = 4
    df.loc[df.maxParty == 'Democrats', "Max"] = 0
    df.loc[df.maxParty == 'Unaffiliated', "Max"] = 2
    df.loc[(df.maxParty == 'Unaffiliated') & (df.Democrats/df.Unaffiliated > partial) , "Max"] = 1
    df.loc[(df.maxParty == 'Unaffiliated') & (df.Republicans/df.Unaffiliated > partial), "Max"] = 3
    df_temp = df[['Republicans', 'Democrats', 'Unaffiliated', 'Republicans', 'Democrats', 'Unaffiliated','maxParty', 'Max' ]]
    print(df_temp.head(20))
    return df

def clean_data(df, df_geo):
    print('cleaning data')
    
    # fill missing data, strings to floats and average thing
    df_transformed = transform_df(df)
    # get total Dems, Reps, Unaffiliated
    df_party_totals = get_totals(df_transformed)
    # per country, find which party has most voters,etc and political leanings
    df_transformed_max = find_max(df_party_totals)
    # join geocoordinates
    df_join = join_geocoordinates(df_transformed_max,df_geo )
    
    return df_join


def get_map_attributes(counties_gdf):
    # prepare data for plot
    lats = counties_gdf['CENT_LAT']
    lons = counties_gdf['CENT_LONG']
    sizes = counties_gdf['Total']/1000.0
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
    for i in range(0,len(counties_gdf['County'])):
        labels.append(counties_gdf['County'][i] + '\nRep: '+reps[i] + '\nUAF: '+uafs[i]+'\nDems: '+dems[i])

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


if __name__ == '__main__':
    df = pd.read_csv('./VotersByPartyStatus.csv')
    filename = './co_counties_voters.geojson'
    file=open(filename)
    counties_gdf = gpd.read_file(file)
    print(counties_gdf.head(1))
    print(counties_gdf.columns)

#create df that contains counties and lat/long for them

    df_counties = counties_gdf[['LABEL', 'CENT_LAT', 'CENT_LONG']]
    df_transformed = transform_df(df)
    df_party_totals = get_totals(df_transformed)
    #print(df_party_totals[['Republicans','REP-Active','REP-Inactive']])
    df_max = find_max(df_party_totals)
    #print(df_max[['Republicans','Democrats','Unaffiliated','maxParty','maxPartyValue']])
    df_join = join_geocoordinates(df_max, df_counties)
    print(df_join.head(2))
    print(df_join.columns)
    