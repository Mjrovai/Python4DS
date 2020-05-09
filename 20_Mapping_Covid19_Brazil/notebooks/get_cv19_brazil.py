'''
# Covid19 - Brazil (Cities) Basic Geographic Analysis
- by Marcelo Rovai
- 27 April 2020

Datasets:
1. Worldometers Daily Data: https://www.worldometers.info/coronavirus/

2. Confirmed cases by day, using information from the news. Covid19br dataset is available at GitHub: https://github.com/wcota/covid19br, 

- Raw data by city compiled from original dataset provided by Brasil.IO (https://brasil.io/dataset/covid19/caso/).

Thanks to: 
- Wesley Cota (https://wesleycota.com), PhD candidate - Complex Networks/Physics (Universidade Federal de Viçosa - Brazil and Universidad de Zaragoza - Spain) 
- Alvaro Justen(https://blog.brasil.io/author/alvaro-justen.html) from Brasil.IO

License: Creative Commons Attribution-ShareAlike 4.0 International
(CC BY-SA 4.0)](https://creativecommons.org/licenses/by-sa/4.0/)

More information: 
- https://wcota.me/covid19br and 
- https://brasil.io/covid19/

run script:
$ python get_cv19_brazil.py

'''

## Main Libraries and setup
print ('\n[INFO] Starting Covid19 - Brazil (Cities) Basic Geographic Analysis - WAIT')

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import plotly
import plotly.graph_objs as go
import geopandas as gpd
from shapely.geometry import Point, Polygon
from unicodedata import normalize
from PIL import Image
import imageio

# Functions used on Brazil Covid-19 Geo Mepping Analysis
from cv_util_func import *

import warnings
warnings.filterwarnings("ignore")

pd.set_option('display.float_format', lambda x: '%.f' % x)
pd.options.display.float_format = '{:,}'.format
mpl.rcParams['figure.dpi']= 150
plt.style.use('seaborn-paper')


## Datasets
print ('\n[INFO] Retriving Covid-19 Brazil Info - WAIT')

worldmetersLink = "https://www.worldometers.info/coronavirus/"
data_wd_covid_br, today = get_wordometers_covid('Brazil', worldmetersLink)

# Saving Brazil info
Total_infected = data_wd_covid_br[0]
New_Cases = data_wd_covid_br[1]
Total_Deaths = data_wd_covid_br[2]
New_Deaths = data_wd_covid_br[3] 
Recovred = data_wd_covid_br[4] 
Active_Case = data_wd_covid_br[5] 
Serious_Critical = data_wd_covid_br[6]
date = today


# Covid19 - Number of total cases by city & State

dt, dt_tm, dt_tm_city, dt_state, total_cases, deaths, cfr = get_brazil_cv_data(
    date)


# Timeline of Brazil Total cases cases
print ('\n[INFO] Plotting Covid-19 Brazil cases')

plot_cases(dt_tm, 'TOTAL', y_scale='linear', n_0=1_000)
plot_cases(dt_tm, 'TOTAL', y_scale='log', n_0=1_000)


# Timeline of cases per top-cities

top_cities = list(dt.sort_values('totalCases', ascending=False)[:10].city)
for city in top_cities:
    plot_cases(dt_tm, city, y_scale='linear', n_0=100)
    plot_cases(dt_tm, city, y_scale='log', n_0=100) 

    
# Timeline New Deaths versus Previus Week    
plot_mov_ave_deaths_last_week(dt_tm, 'TOTAL', y_scale='linear', n_0=100, mov=7, show=False, save=True)   

for city in top_cities:
    plot_mov_ave_deaths_last_week(dt_tm, city, y_scale='linear', n_0=1, mov=7, show=False, save=True)
    
      
# GeoData (Brasil & Municipalities)
print ('\n[INFO] Getting Brazilian Geodata\n') 

br_shp, br_cities = load_geodata()


# Maping CoronaVirus data
print ('\n[INFO] Mapping Covid-19 Brazil cases - WAIT \n')

# Nationwide Analysis
date = datetime.datetime.today()
cv_city, deaths_city, cv_city_pnt, deaths_city_pnt, total_cases, deaths, cfr = get_Brazil_data(dt, br_shp, br_cities)
plt_Brasil_cities(cv_city, deaths_city, date, total_cases, deaths, cfr, br_shp, br_cities, deaths_only=False)
plt_Brasil_cv_metrics(cv_city_pnt, deaths_city_pnt, date, total_cases, deaths, cfr, br_shp, br_cities)
plt_Brasil_cv_metrics(cv_city_pnt, deaths_city_pnt, date, total_cases, deaths, cfr, br_shp, br_cities, metrics='deaths', n=4)

# Other Pandemic metrics maps
plt_Brasil_cv_metrics(cv_city_pnt, deaths_city_pnt, date, total_cases, deaths, cfr, br_shp, br_cities, metrics='TotalCases/1M pop', n=2 )
plt_Brasil_cv_metrics(cv_city_pnt, deaths_city_pnt, date, total_cases, deaths, cfr, br_shp, br_cities, metrics='Deaths/1M pop', n=5 )
plt_Brasil_cv_metrics(cv_city_pnt, deaths_city_pnt, date, total_cases, deaths, cfr, br_shp, br_cities, metrics='CFR[%]', n=5 )


# Selected State Analysis
print ('\n[INFO] Mapping Covid-19 Brazil state cases - WAIT \n')

cv_sp, deaths_sp, sp_total_cases, sp_deaths = get_state_info(cv_city, dt_state, br_shp, br_cities, 'SP')
cv_rj, deaths_rj, rj_total_cases, rj_deaths = get_state_info(cv_city, dt_state, br_shp, br_cities, 'RJ')
cv_mg, deaths_mg, mg_total_cases, mg_deaths = get_state_info(cv_city, dt_state, br_shp, br_cities, 'MG')
cv_ce, deaths_ce, ce_total_cases, ce_deaths = get_state_info(cv_city, dt_state, br_shp, br_cities, 'CE')

     
# Creating Gifs
print ('\n[INFO] Creating GIFs - WAIT ', end =" ")  

cv_city_t = pd.merge(br_cities, dt_tm_city, on='COD. IBGE')
deaths_city_t = cv_city_t.loc[cv_city_t['deaths'] != 0].copy()
dates = list(set(cv_city_t.date))
dates.sort()
dates = dates[-2:] 

create_state_gif(dates, cv_city_t, deaths_city_t, br_shp, 'BR') ; print ('.', end =" ") 
create_state_gif(dates, cv_city_t, deaths_city_t, br_shp, 'SP'); print ('.', end =" ") 
create_state_gif(dates, cv_city_t, deaths_city_t, br_shp, 'RJ'); print ('.', end =" ") 
create_state_gif(dates, cv_city_t, deaths_city_t, br_shp, 'MG'); print ('.', end =" ") 
create_state_gif(dates, cv_city_t, deaths_city_t, br_shp, 'CE'); print ('.')


### Creating videos from Gifs
print ('\n[INFO] Creating Movies - WAIT ', end =" ") 

conv_gif_to_mp4('BR', fps=5); print ('.', end =" ") 
conv_gif_to_mp4('SP', fps=5); print ('.', end =" ") 
conv_gif_to_mp4('RJ', fps=5); print ('.', end =" ") 
conv_gif_to_mp4('MG', fps=5); print ('.', end =" ") 
conv_gif_to_mp4('CE', fps=5); print ('.') 

print ('\n[INFO] End script MJRoBot.org @ {}\n'.format(today)) 


