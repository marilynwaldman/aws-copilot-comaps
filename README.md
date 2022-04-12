# Map that read Colorado csv - must contain these fields:
1.  Index(['County',  'DEM-Active', 
        'REP-Active', 'UAF-Active', 
         'Total-Active',
        'DEM-Inactive',
       'REP-Inactive', 'UAF-Inactive',
       'Total', 
2.  Geopandas file draws polygons for counties and is used to get lat/lon to joing with df above:
        'LABEL' - county name
        'CENT_LAT',
       'CENT_LONG',
  
To Dockerize

```
cd aws-copilot-comaps/services/copoliticalmap
docker build -t comap .
docker run --rm --name query -p 8050:8050 comap

```