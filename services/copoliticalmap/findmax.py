import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import geopandas as gpd
import base64
import datetime
import io
import numpy as np

matrix = [(10, 56, 17),
          (4.0, 23, 11),
          (49, 36, 55),
          (75, 10.0, 34),
          (89, 21, 44)
          ]
# Create a DataFrame
df = pd.DataFrame(matrix, index = list('abcde'), columns = list('xyz'))
print(df)

maxValues = df[['x', 'y', 'z']].max(axis = 1)

print(maxValues)

maxValueIndex = df.idxmax(axis = 1)

print(maxValueIndex)