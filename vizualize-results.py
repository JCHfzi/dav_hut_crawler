#%% Load Data

import pandas as pd
df = pd.read_csv("collected_data/alle_huetten.csv") 
df

#%% Transform Swiss Coordinates


from pyproj import Proj



swiss = Proj(init='EPSG:21781')
swiss(600000, 200000, inverse=True)


# Create Lat Long from Swiss Data
df_extracted_swiss = df['Coordinates'].str.split('/', expand=True)

df_extracted_swiss[0] = df_extracted_swiss[0].str.replace(".","").apply(pd.to_numeric, errors='coerce')
df_extracted_swiss[1] = df_extracted_swiss[1].str.replace(".","").apply(pd.to_numeric, errors='coerce')
df_extracted_swiss

df_extracted_swiss = df_extracted_swiss.assign(Lat = lambda x: (swiss(x[0], x[1], inverse=True)[1]))
df_extracted_swiss = df_extracted_swiss.assign(Long = lambda x: (swiss(x[0], x[1], inverse=True)[0]))
df_extracted_swiss

# Bring back to original Data Frame
df["Lat"]=df_extracted_swiss["Lat"]
df["Long"]=df_extracted_swiss["Long"]
df

# %% Plot Data

import plotly.express as px


fig = px.scatter_mapbox(df, lat="Lat", lon="Long", hover_name="Hütten-Name", hover_data=["Hütte-ID", "Total sleeping places","Height above sea level"],
                        color_discrete_sequence=["fuchsia"], zoom=3, height=300)
fig.update_layout(mapbox_style="open-street-map")
#fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()

### Concat Data to Show Free Huts


# %%
