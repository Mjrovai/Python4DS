#! /usr/bin/env python
'''
Functions to be used on Brazil Covid-19 Geo Mepping Analysis
Developed by Marcelo Rovai
April, 26 2020

To use call: from cv_util_func import *
'''
import time
import datetime
import requests
from bs4 import BeautifulSoup
import glob
from PIL import Image
import imageio

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import plotly
import plotly.graph_objs as go
import geopandas as gpd
from shapely.geometry import Point, Polygon
from unicodedata import normalize

'''
Functions for getting, show and plotting CV-19 dataset

'''
def plot_cases(data,
               city,
               n_0=100,
               y_scale='log',
               mov=7,
               show=False,
               save=True):
    date = datetime.datetime.today()
    data = data[data.city == city]
    tst = data[data.totalCases >= n_0]
    tst['totalCases_Mov_Ave'] = tst.iloc[:, 8].rolling(window=mov).mean()
    tst['newCases_Mov_Ave'] = tst.iloc[:, 7].rolling(window=mov).mean()
    tst['deaths_Mov_Ave'] = tst.iloc[:, 6].rolling(window=mov).mean()
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=tst.date, y=round(tst.totalCases_Mov_Ave), name='Total Cases', line=dict(color='royalblue', width=2)))
    fig.add_trace(go.Scatter(x=tst.date, y=round(tst.newCases_Mov_Ave), name='New Cases', line=dict(color='orange', width=2)))
    fig.add_trace(go.Scatter(x=tst.date, y=round(tst.deaths_Mov_Ave), name='Deaths', line=dict(color='firebrick', width=2)))
    fig.update_layout(
        title='Covid-19 Brazil ({}) - {}/{}/{}'
        .format(city, date.year, date.month, date.day),
        xaxis_title="Day",
        yaxis_title="Number of Cases",
        yaxis_type=y_scale,
        font=dict(size=10, color="#7f7f7f"),
        legend=dict(x=0,
                    y=1.0,
                    bgcolor='rgba(255, 255, 255, 0)',
                    bordercolor='rgba(255, 255, 255, 0)'),
        annotations=[
            dict(x=0,
                 y=1.05,
                 text='Cases over {:,} - Y-scale: {} ({}-day rolling avg.)'
                 .format(n_0, y_scale, mov),
                 showarrow=False,
                 xref='paper',
                 yref='paper',
                 xanchor='left',
                 yanchor='auto',
                 xshift=0,
                 yshift=0,
                 font=dict(size=10, color="#7f7f7f")),
            dict(x=1,
                 y=-0.10,
                 text="Source: Brasil.io - https://brasil.io/dataset/covid19/caso/",
                 showarrow=False,
                 xref='paper',
                 yref='paper',
                 xanchor='right',
                 yanchor='auto',
                 xshift=0,
                 yshift=0,
                 font=dict(size=8, color='royalblue')),
            dict(x=1,
                 y=-0.14,
                 text="Created by Marcelo Rovai - https://MJRoBot.org",
                 showarrow=False,
                 xref='paper',
                 yref='paper',
                 xanchor='right',
                 yanchor='auto',
                 xshift=0,
                 yshift=0,
                 font=dict(size=8, color='royalblue'))
        ])

    if save == True:
        city = city.replace('/', '-')
        fig.write_image('../graphs/cv19_' + city + '_' + y_scale +
                        '_CV_Evolution_Graph_updated.png')
    if show == True:
        fig.show()

# -------------------------------------------------------------------------------------    

def plot_mov_ave_deaths_last_week(data,
               city,
               n_0=100,
               y_scale='log',
               mov=7,
               show=False,
               save=True):
    date = datetime.datetime.today()
    data = data[data.city == city]
    tst = data[data.deaths >= n_0]
    tst.reset_index(drop=True, inplace = True)

    tst['new_deaths'] = tst['deaths'] - tst['deaths'].shift(1)
    tst['new_deaths_Mov_Ave'] = tst.iloc[:, -1].rolling(window=mov).mean()
    tst['mov_ave_new_deaths_last_week'] = tst['new_deaths_Mov_Ave'] - tst['new_deaths_Mov_Ave'].shift(7)
    fig = go.Figure()
    fig.add_trace(go.Bar(x=tst.date, y=round(tst.new_deaths_Mov_Ave), name='New Deaths'))
    fig.add_trace(go.Bar(x=tst.date, y=round(tst.mov_ave_new_deaths_last_week), name='New Deaths vs last week'))
    fig.update_layout(
        title='Brazil ({}) - New Deaths by Covid-19 versus same day previous week'
        .format(city),
        xaxis_title="Day",
        yaxis_title="Number of Deaths",
        yaxis_type=y_scale,
        font=dict(size=10, color="#7f7f7f"),
        legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
        annotations=[
            dict(x=0,
                 y=1.05,
                 text='Deaths over {:,} - Y-scale: {} ({}-day rolling average) - {}/{}/{}'
                 .format(n_0, y_scale, mov, date.year, date.month, date.day),
                 showarrow=False,
                 xref='paper',
                 yref='paper',
                 xanchor='left',
                 yanchor='auto',
                 xshift=0,
                 yshift=0,
                 font=dict(size=10, color="#7f7f7f")),
            dict(x=1,
                 y=-0.10,
                 text="Source: Brasil.io - https://brasil.io/dataset/covid19/caso/",
                 showarrow=False,
                 xref='paper',
                 yref='paper',
                 xanchor='right',
                 yanchor='auto',
                 xshift=0,
                 yshift=0,
                 font=dict(size=8, color='royalblue')),
            dict(x=1,
                 y=-0.14,
                 text="Created by Marcelo Rovai - https://MJRoBot.org",
                 showarrow=False,
                 xref='paper',
                 yref='paper',
                 xanchor='right',
                 yanchor='auto',
                 xshift=0,
                 yshift=0,
                 font=dict(size=8, color='royalblue'))
        ])

    if save == True:
        city = city.replace('/', '-')
        fig.write_image('../graphs/cv19_' + city + '_' + y_scale +
                        '_CV_Mov_ave_deaths_last_week_Evolution_Graph_updated.png')
    if show == True:
        fig.show()
# -------------------------------------------------------------------------------------    

def data_cleanup(array):
    L = []
    for i in array:
        i = i.replace("+","")
        i = i.replace("-","")
        i = i.replace(",",".")
        if i == "":
            i = "0"
        L.append(i.strip())
    return L



def get_wordometers_covid(country, worldmetersLink):
    today = datetime.datetime.today()
    try:
        html_page = requests.get(worldmetersLink)
    except requests.exceptions.RequestException as e: 
        print(e) #ConnectionError
    bs = BeautifulSoup(html_page.content, 'html.parser')
    search = bs.select("div tbody tr td")
    start = -1
    for i in range(len(search)):
        if search[i].get_text().find(country) !=-1:
            start = i
            break
    data = []
    for i in range(1,8):
        try:
            data = data + [search[start+i].get_text()]
        except:
            data = data + ["0"]

    data = data_cleanup(data)

    print('\n{} - Worldometers Daily Data\n'.format(country))
    print(
        "Today is {} \n- Total infected = {} \n- New Cases = {} \n- Total Deaths = {} \n- New Deaths = {} \n- Recovered = {} \n- Active Cases = {} \n- Serious-Critical = {}"
        .format(today, *data))
    return data, today


def get_brazil_cv_data(date):

    url = 'https://raw.githubusercontent.com/wcota/covid19br/master/cases-brazil-cities.csv'
    url_tm = 'https://raw.githubusercontent.com/wcota/covid19br/master/cases-brazil-cities-time.csv'
    dt = pd.read_csv(url, error_bad_lines=False)
    dt_tm = pd.read_csv(url_tm, error_bad_lines=False)
    print("\nToday is {}/{}/{}. Dataset with {} observations.\n".format(
        date.year, date.month, date.day, dt.shape[0]))
    
    file = '../data/cases-brazil-cities-'+str(date.day)+'-'+str(date.month)+'-'+str(date.year)+'.csv'
    dt.to_csv(file)
    
    dt.rename(columns={'ibgeID':'COD. IBGE'}, inplace=True)
    total_cases = dt.totalCases.sum()
    deaths = dt.deaths.sum()
    cfr = round ((deaths/total_cases)*100, 2)
    print('\nTotal number of cases in Brasil at {}/{}: {:,} ({} fatal) with a CFR of {}%'.format(
    date.month, date.day, total_cases, deaths, cfr))
    dt['CFR[%]'] = round((dt.deaths/dt.totalCases)*100, 2)
    dt.fillna(0, inplace=True)
    
    dt_state = dt.groupby('state')[['deaths','totalCases']].sum().reset_index()
    dt_state['CFR[%]'] = round((dt_state.deaths/dt_state.totalCases)*100, 2)
    
    dt_tm_city = dt_tm.loc[(dt_tm['state'] != 'TOTAL')].copy()
    dt_tm_city.rename(columns={'ibgeID':'COD. IBGE'}, inplace=True)

    return dt, dt_tm, dt_tm_city, dt_state, total_cases, deaths, cfr

'''
Functions for getting Brazil Geodata
'''

def load_geodata():
    # Brazil by States
    br_shp = gpd.read_file(
        '../data/10_geodata/20_Brazil_by_State/Brazil_Dataset_By_State.shp',
        encoding='utf-8')

    br_cities = gpd.read_file(
        '../data/10_geodata/10_Brazil_by_City/Brazil_Dataset_By_City.shp',
        encoding='utf-8')

    # Brazil by States
    br_cities.rename(columns={
        'NOME DO MU': 'City',
        'POPULAÇÃ': 'POP_2019',
    },
                     inplace=True)

    print('Number of Brazilian Cities: {:,}'.format(len(br_cities.index)))
    print('Total Brazilian Population: {:,}'.format(
        br_cities['POP_2019'].sum()))
    print('Total Brazilian Territory : {:,} km2 (aprox.)'.format(
        round(br_cities['AREA APROX'].sum())))
    print('Average Demografic Density : {:,} hab/km2 (aprox.)'.format(
        round(
            (br_cities['POP_2019'].sum()) / (br_cities['AREA APROX'].sum()))))
    
    return br_shp, br_cities

def load_roads():
    sp_motorway = gpd.read_file(
        '../data/10_geodata/35_main_roads_by_state/sp_motorway.shp',
        encoding='utf-8')
    sp_primary = gpd.read_file(
        '../data/10_geodata/35_main_roads_by_state/sp_primary.shp',
        encoding='utf-8')

    rj_motorway = gpd.read_file(
        '../data/10_geodata/35_main_roads_by_state/rj_motorway.shp',
        encoding='utf-8')
    rj_primary = gpd.read_file(
        '../data/10_geodata/35_main_roads_by_state/rj_primary.shp',
        encoding='utf-8')

    mg_motorway = gpd.read_file(
        '../data/10_geodata/35_main_roads_by_state/mg_motorway.shp',
        encoding='utf-8')
    mg_primary = gpd.read_file(
        '../data/10_geodata/35_main_roads_by_state/mg_primary.shp',
        encoding='utf-8')

    ce_motorway = gpd.read_file(
        '../data/10_geodata/35_main_roads_by_state/ce_motorway.shp',
        encoding='utf-8')
    ce_primary = gpd.read_file(
        '../data/10_geodata/35_main_roads_by_state/ce_primary.shp',
        encoding='utf-8')
    return sp_motorway, sp_primary, rj_motorway, rj_primary, mg_motorway, mg_primary, ce_motorway, ce_primary


'''
Functions for Mapping CV-9'
'''

def get_Brazil_data(dt, br_shp, br_cities):
    total_cases = dt.totalCases.sum()
    deaths = dt.deaths.sum()
    cfr = round((deaths / total_cases) * 100, 2)
    date = datetime.datetime.today()
    cv_city = pd.merge(br_cities, dt, on='COD. IBGE')
    cv_city['TotalCases/1M pop'] = round(
        cv_city.totalCases / (cv_city['POP_2019'] / 1000_000), 1)
    cv_city['Deaths/1M pop'] = round(
        cv_city.deaths / (cv_city['POP_2019'] / 1000_000), 1)
    deaths_city = cv_city.loc[cv_city['deaths'] != 0].copy()
    cv_city_pnt = cv_city.copy()
    cv_city_pnt['geometry'] = cv_city_pnt['geometry'].representative_point()
    deaths_city_pnt = cv_city_pnt[cv_city_pnt.deaths != 0]
    print(
        'Brazil: Total number of Covid19 cases at {}/{}: {:,} ({:,} fatal) in {:,} cities with a CFR of {}%'
        .format(date.month, date.day, total_cases, deaths, len(cv_city.index),
                cfr))

    dt_city = cv_city_pnt.sort_values('totalCases', ascending=False).copy()
    dt_city = dt_city[[
        'City', 'UF', 'POP_2019', 'AREA APROX', 'DENS. DEMO', 'totalCases',
        'deaths', 'CFR[%]', 'TotalCases/1M pop', 'Deaths/1M pop'
    ]].reset_index(drop=True)
    dt_city.index += 1
    file = '../data/20_Covid_Database_Brazil/cv19_Brazil_' + str(
        date.month) + '-' + str(date.day) + '-' + str(date.year) + '.xlsx'
    dt_city.to_excel(file)

    return cv_city, deaths_city, cv_city_pnt, deaths_city_pnt, total_cases, deaths, cfr

def plt_Brasil_cities(cv_city,
                      deaths_city,
                      date,
                      total_cases,
                      deaths,
                      cfr,
                      br_shp, br_cities,
                      deaths_only=False):
    ax = br_shp.plot(figsize=(18, 16), color='#FFFFFF', edgecolor='#444444')
    if deaths_only == False:
        cv_city.plot(ax=ax, color="orange", markersize=5, label='City')
    deaths_city.plot(ax=ax,
                     color="red",
                     markersize=5,
                     label='City with Deaths')
    plt.title(
        'Brazil: Covid19 total cases at {}/{}/{}: {:,} ({:,} fatal in red) in {:,} identified cities\
        \nCFR: {}% - Total data includes cases/deaths with not identified cities'
        .format(date.year, date.month, date.day, total_cases, deaths,
                len(cv_city.index), cfr),
        fontsize=20,
        loc='left')
    plt.axis('off')

    for idx, row in br_shp.iterrows():
        plt.annotate(s=row['UF'],
                     xy=(row.geometry.centroid.x, row.geometry.centroid.y),
                     horizontalalignment='center',
                     fontsize=10,
                     color='green')

    plt.annotate('Map created by Marcelo Rovai (MJRoBot.org) @{}/{}/{}'.format(
        date.year, date.month, date.day),
                 xy=(0.55, .17),
                 xycoords='figure fraction',
                 horizontalalignment='left',
                 fontsize=12,
                 color='blue')
    plt.annotate('Data provided by https://brasil.io/dataset/covid19/caso/',
                 xy=(0.55, .16),
                 xycoords='figure fraction',
                 horizontalalignment='left',
                 fontsize=12,
                 color='blue')
    plt.annotate(
        'License: CC BY-SA 4.0 (https://creativecommons.org/licenses/by-sa/4.0/',
        xy=(0.55, .15),
        xycoords='figure fraction',
        horizontalalignment='left',
        fontsize=12,
        color='blue')

    file_today = '../images/!cv19_BR_last_updated.png'
    file = '../images/cv19_Brazil_' + str(date.month) + '-' + str(
        date.day) + '-' + str(date.year) + '.png'
    #file_gif = '../br_images_gif/today_cv19_Brazil.png'

    if deaths_only == False:
        plt.savefig(file, dpi=300)
        plt.savefig(file_today, dpi=300)
        #plt.savefig(file_gif, dpi=200)


def plt_Brasil_cv_metrics(cv_city_pnt,
                          deaths_city_pnt,
                          date,
                          total_cases,
                          deaths,
                          cfr,
                          br_shp, br_cities,
                          metrics='totalCases',
                          n=4):
    ax = br_shp.plot(figsize=(18, 16), color='#FFFFFF', edgecolor='#444444')
    cv_city_pnt.plot(ax=ax,
                     color='orange',
                     markersize=n * cv_city_pnt[metrics],
                     alpha=.5)
    
    if metrics == 'totalCases':
        deaths_city_pnt.plot(ax=ax,
                             color='black',
                             marker='+',
                             alpha=.5,
                             markersize=100,
                             label='Deaths')
        ax.legend(fontsize=15)
        plt.title(
            'Brazil: Covid19 total cases at {}/{}/{}: {:,} ({:,} fatal) in {:,} identified cities\
            \nCFR of {}% - Total data includes cases/deaths with not identified cities'
            .format(date.year, date.month, date.day, total_cases, deaths,
                    len(cv_city_pnt.index), cfr),
            fontsize=20,
            loc='left')
    elif metrics == 'CFR[%]':
        plt.title(
            'Covid19 Case Fatality Rate (CFR[%]) per city in Brazil at {}/{}/{}'
            .format(date.year, date.month, date.day),
            fontsize=20,
            loc='left')
    elif metrics == 'TotalCases/1M pop':
        plt.title(
            'Covid19 Total Cases per each 1 Million inhabitants per city in Brazil at {}/{}/{}'
            .format(date.year, date.month, date.day),
            fontsize=20,
            loc='left')
    elif metrics == 'Deaths/1M pop':
        plt.title(
            'Covid19 Deaths per each 1 Million inhabitants per city in Brazil at {}/{}/{}'
            .format(date.year, date.month, date.day),
            fontsize=20,
            loc='left')
    elif metrics == 'deaths':
        plt.title(
            'Covid19 Accumulated Deaths per city in Brazil at {}/{}/{}'
            .format(date.year, date.month, date.day),
            fontsize=20,
            loc='left')

    plt.axis('off')

    for idx, row in br_shp.iterrows():
        plt.annotate(s=row['UF'],
                     xy=(row.geometry.centroid.x, row.geometry.centroid.y),
                     horizontalalignment='center',
                     fontsize=10,
                     color='green')

    plt.annotate('Map created by Marcelo Rovai (MJRoBot.org) @{}/{}/{}'.format(
        date.year, date.month, date.day),
                 xy=(0.55, .15),
                 xycoords='figure fraction',
                 horizontalalignment='left',
                 fontsize=12,
                 color='blue')
    plt.annotate('Data provided by https://brasil.io/dataset/covid19/caso/',
                 xy=(0.55, .14),
                 xycoords='figure fraction',
                 horizontalalignment='left',
                 fontsize=12,
                 color='blue')
    plt.annotate(
        'License: CC BY-SA 4.0 (https://creativecommons.org/licenses/by-sa/4.0/',
        xy=(0.55, .13),
        xycoords='figure fraction',
        horizontalalignment='left',
        fontsize=12,
        color='blue')

    metrics = metrics.replace('/', '_per_')
    metrics = metrics.replace(' ', '_')

    file_today = '../images/!cv19_BR_CV_' + metrics + '_last_updated.png'
    file = '../images/cv19_Brazil_CV_' + metrics + '_' + str(
        date.month) + '-' + str(date.day) + '-' + str(date.year) + '.png'
    plt.savefig(file, dpi=300)
    plt.savefig(file_today, dpi=300)
    

def get_state_info(cv_city, dt_state, br_shp, br_cities, state):
    date = datetime.datetime.today()
    
    cv_state = cv_city.loc[cv_city['UF'] == state].copy()
    deaths_state = cv_state.loc[cv_state['deaths'] != 0].copy()
    state_total_cases = dt_state[dt_state.state == state].totalCases.sum()
    state_deaths = dt_state[dt_state.state == state].deaths.sum()
    print(
        'Total number of Covid19 cases reported in {} State at {}/{}: {:,} ({:,} fatal) in {:,} specified cities'
        .format(state, date.month, date.day, state_total_cases, state_deaths,
                len(cv_state.index)))
    plot_state_cases(state, cv_state, deaths_state, state_total_cases, state_deaths, date, br_shp, br_cities)
    dt_state = cv_state.sort_values('totalCases', ascending=False).copy()
    dt_state = dt_state[[
        'City', 'UF', 'POP_2019', 'AREA APROX',
        'DENS. DEMO', 'totalCases', 'deaths'
    ]].reset_index(drop=True)
    dt_state.index += 1
    return cv_state, deaths_state, state_total_cases, state_deaths


def plot_state_cases(state, cv_state, deaths_state, state_total_cases,
                     state_deaths, date, br_shp, br_cities):
    sp_motorway, sp_primary, rj_motorway, rj_primary, mg_motorway, mg_primary, ce_motorway, ce_primary = load_roads(
)
    
    if state == 'SP':
        sp_shp = br_shp.loc[br_shp['UF'] == state].copy()
        ax = sp_shp.plot(figsize=(18, 16),
                         color='#FFFFFF',
                         edgecolor='#444444')
        sp_motorway.plot(ax=ax, color="green", markersize=1, label='Motorway')
        sp_primary.plot(ax=ax,
                        color="#E8E8E8",
                        markersize=1,
                        label='Primary Roads')
        xy_1 = (-47.2, -25)
        xy_2 = (-47.2, -25.1)
        xy_3 = (-47.2, -25.2)
    if state == 'RJ':
        rj_shp = br_shp.loc[br_shp['UF'] == state].copy()
        ax = rj_shp.plot(figsize=(18, 16),
                         color='#FFFFFF',
                         edgecolor='#444444')
        rj_motorway.plot(ax=ax, color="green", markersize=1, label='Motorway')
        rj_primary.plot(ax=ax,
                        color="#E8E8E8",
                        markersize=1,
                        label='Primary Roads')
        xy_1 = (-42.3, -23.1)
        xy_2 = (-42.3, -23.15)
        xy_3 = (-42.3, -23.2)
    if state == 'MG':
        mg_shp = br_shp.loc[br_shp['UF'] == state].copy()
        ax = mg_shp.plot(figsize=(18, 16),
                         color='#FFFFFF',
                         edgecolor='#444444')
        mg_motorway.plot(ax=ax, color="green", markersize=1, label='Motorway')
        mg_primary.plot(ax=ax,
                        color="#E8E8E8",
                        markersize=1,
                        label='Primary Roads')
        xy_1 = (-44.7, -22.8)
        xy_2 = (-44.7, -22.95)
        xy_3 = (-44.7, -23.1)

    if state == 'CE':
        ce_shp = br_shp.loc[br_shp['UF'] == state].copy()
        ax = ce_shp.plot(figsize=(18, 16),
                         color='#FFFFFF',
                         edgecolor='#444444')
        ce_motorway.plot(ax=ax, color="green", markersize=1, label='Motorway')
        ce_primary.plot(ax=ax,
                        color="#E8E8E8",
                        markersize=1,
                        label='Primary Roads')
        xy_1 = (-39, -7.95)
        xy_2 = (-39, -8.01)
        xy_3 = (-39, -8.07)

    cv_state.plot(ax=ax, color="orange", markersize=5, label='City')
    deaths_state.plot(ax=ax,
                      color="red",
                      markersize=5,
                      label='City with Deaths')

    plt.title(
        'Covid19 total cases reported in {} State at {}/{}/{}: {:,} ({:,} fatal in red) in {:,} identified cities\
        \nTotal data includes cases/deaths with not identified cities'.format(
            state, date.year, date.month, date.day, state_total_cases,
            state_deaths, len(cv_state.index)),
        fontsize=20,
        loc='left')
    plt.axis('off')
    ax.legend(fontsize=15)

    plt.annotate('Map created by Marcelo Rovai (MJRoBot.org) @{}/{}/{}'.format(
        date.year, date.month, date.day),
                 xy=xy_1,
                 fontsize=10,
                 color='blue')
    plt.annotate('Data provided by https://brasil.io/dataset/covid19/caso/',
                 xy=xy_2,
                 fontsize=10,
                 color='blue')
    plt.annotate(
        'License: CC BY-SA 4.0 (https://creativecommons.org/licenses/by-sa/4.0/)',
        xy=xy_3,
        fontsize=10,
        color='blue')

    file_today = '../images/!cv19_' + state + '_last_updated.png'
    plt.savefig(file_today, dpi=300)
    file = '../images/cv19_' + state + '_' + str(date.month) + '-' + str(
        date.day) + '-' + str(date.year) + '.png'
    plt.savefig(file, dpi=300)

    #file_gif = '../'+state.lower()+'_images_gif/today_cv19_' + state.lower() + '.png'
    #plt.savefig(file_gif, dpi=200)
    

'''
Functions for creating Movie
'''

def conv_gif_to_mp4(state, fps=5, colour=True):
    gif_in = '../gifs/gifs/'+state+'_Covid-19_Timeline.gif'
    vid_out = '../videos/'+state+'_Covid-19_Timeline'
    reader = imageio.get_reader(gif_in)
    writer = imageio.get_writer(vid_out+'.mp4', fps=fps)
    for im in reader:
        if colour == True:
            writer.append_data(im)
        else:    
            writer.append_data(im[:, :, 1])
    writer.close()

def save_gifs (state):
    frames = []
    imgs = sorted(glob.glob('../gifs/'+state.lower()+'_images_gif/*.png'))
    for i in imgs:
        frames.append(imageio.imread(i))
    imageio.mimsave('../gifs/gifs/'+state+'_Covid-19_Timeline.gif', frames)

def create_state_gif(dates, cv_city_t, deaths_city_t, br_shp, state):
    
    sp_motorway, sp_primary, rj_motorway, rj_primary, mg_motorway, mg_primary, ce_motorway, ce_primary = load_roads()

    for date in dates:

        if state == 'BR':
            ax = br_shp.plot(figsize=(18, 16),
                               color='#FFFFFF',
                               edgecolor='#444444')
            fdtt = cv_city_t.loc[cv_city_t['date'] == date].copy()
            fdtt_deaths = deaths_city_t.loc[deaths_city_t['date'] == date].copy()
            fdtt.plot(ax=ax, color="orange", markersize=5, label='City')              
            fdtt_deaths.plot(ax=ax, color="red", markersize=5, label='death')
            plt.title('Brazilian cities reported with Covid19 cases (orange) and deaths (red))', fontsize=30)
            for idx, row in br_shp.iterrows():
                plt.annotate(s=row['UF'],
                             xy=(row.geometry.centroid.x,
                                 row.geometry.centroid.y),
                             horizontalalignment='center',
                             fontsize=10,
                             color='green')

            xy_a = (0.7, .85)
            xy_b = (0.7, .82)
            xy_c = (0.7, .79)
            xy_d = (0.7, .76)
            xy_1 = (-48.8, -32.7)
            xy_2 = (-48.8, -33.2)
            xy_3 = (-48.8, -33.7)

        if state == 'SP':
            sp_shp = br_shp.loc[br_shp['UF'] == state].copy()
            ax = sp_shp.plot(figsize=(18, 16),
                             color='#FFFFFF',
                             edgecolor='#444444')
            sp_motorway.plot(ax=ax,
                             color="green",
                             markersize=1,
                             label='Motorway')
            sp_primary.plot(ax=ax,
                            color="#E8E8E8",
                            markersize=1,
                            label='Primary Roads')

            xy_a = (0.7, .72)
            xy_b = (0.7, .69)
            xy_c = (0.7, .66)
            xy_d = (0.7, .63)
            xy_1 = (-47.2, -25)
            xy_2 = (-47.2, -25.1)
            xy_3 = (-47.2, -25.2)

        if state == 'RJ':
            rj_shp = br_shp.loc[br_shp['UF'] == state].copy()
            ax = rj_shp.plot(figsize=(18, 16),
                             color='#FFFFFF',
                             edgecolor='#444444')
            rj_motorway.plot(ax=ax,
                             color="green",
                             markersize=1,
                             label='Motorway')
            rj_primary.plot(ax=ax,
                            color="#E8E8E8",
                            markersize=1,
                            label='Primary Roads')

            xy_a = (0.2, .72)
            xy_b = (0.2, .69)
            xy_c = (0.2, .66)
            xy_d = (0.2, .63)
            xy_1 = (-42.3, -23.1)
            xy_2 = (-42.3, -23.15)
            xy_3 = (-42.3, -23.2)
            
        if state == 'MG':
            mg_shp = br_shp.loc[br_shp['UF'] == state].copy()
            ax = mg_shp.plot(figsize=(18, 16),
                             color='#FFFFFF',
                             edgecolor='#444444')
            mg_motorway.plot(ax=ax,
                             color="green",
                             markersize=1,
                             label='Motorway')
            mg_primary.plot(ax=ax,
                            color="#E8E8E8",
                            markersize=1,
                            label='Primary Roads')
            xy_a = (0.1, .72)
            xy_b = (0.1, .69)
            xy_c = (0.1, .66)
            xy_d = (0.1, .63)
            xy_1 = (-44.7, -22.8)
            xy_2 = (-44.7, -22.95)
            xy_3 = (-44.7, -23.1)

        if state == 'CE':
            ce_shp = br_shp.loc[br_shp['UF'] == state].copy()
            ax = ce_shp.plot(figsize=(18, 16),
                             color='#FFFFFF',
                             edgecolor='#444444')
            ce_motorway.plot(ax=ax,
                             color="green",
                             markersize=1,
                             label='Motorway')
            ce_primary.plot(ax=ax,
                            color="#E8E8E8",
                            markersize=1,
                            label='Primary Roads')
            xy_a = (0.7, .75)
            xy_b = (0.7, .72)
            xy_c = (0.7, .69)
            xy_d = (0.7, .66)
            xy_1 = (-39, -7.95)
            xy_2 = (-39, -8.01)
            xy_3 = (-39, -8.07)

        if state != 'BR':
            cv_state_t = cv_city_t.loc[cv_city_t['state'] == state].copy()
            deaths_state_t = deaths_city_t.loc[deaths_city_t['state'] == state].copy()
            fdtt = cv_state_t.loc[cv_state_t['date'] == date].copy()
            fdtt_deaths = deaths_state_t.loc[deaths_state_t['date'] == date].copy()
            fdtt.plot(ax=ax, color="orange", markersize=5, label='City')
            fdtt_deaths.plot(ax=ax, color="red", markersize=5, label='City')
            plt.title(state + ' state cities reported with Covid19 cases (orange) and deaths (red)',
                      fontsize=30)

        plt.annotate('Date:         {}'.format(date),
                     xy=xy_a,
                     xycoords='figure fraction',
                     horizontalalignment='left',
                     verticalalignment='top',
                     fontsize=25)

        plt.annotate('Total Cases:        {}'.format(str(
            fdtt.totalCases.sum())),
                     xy=xy_b,
                     xycoords='figure fraction',
                     horizontalalignment='left',
                     verticalalignment='top',
                     fontsize=25)
        plt.annotate('Total deaths:        {}'.format(str(
            fdtt_deaths.deaths.sum())),
                     xy=xy_c,
                     xycoords='figure fraction',
                     horizontalalignment='left',
                     verticalalignment='top',
                     fontsize=25)

        plt.annotate('Number of Cities:  {}'.format(str(len(fdtt.index))),
                     xy=xy_d,
                     xycoords='figure fraction',
                     horizontalalignment='left',
                     verticalalignment='top',
                     fontsize=25)
        plt.annotate('Map created by Marcelo Rovai (MJRoBot.org) ',
                     xy=xy_1,
                     fontsize=10,
                     color='blue')
        plt.annotate(
            'Data provided by https://brasil.io/dataset/covid19/caso/',
            xy=xy_2,
            fontsize=10,
            color='blue')
        plt.annotate(
            'License: CC BY-SA 4.0 (https://creativecommons.org/licenses/by-sa/4.0/)',
            xy=xy_3,
            fontsize=10,
            color='blue')

        plt.axis('off')
        file = '../gifs/' + state.lower() + '_images_gif/cv19_' + state + '_' + str(
            date) + '.png'
        plt.savefig(file, dpi=200)

    save_gifs(state)