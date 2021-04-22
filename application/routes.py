__author__ = 'nahla.errakik'

import os
import folium
import datetime
from pathlib import Path
from flask import render_template
from application import app
from application.models import Case
from application.utils import helpers


@app.route("/")
def index():
    last_update = Case.get_last_update()
    if last_update is None:
        helpers.insert_db()
    elif last_update[0].date() < datetime.datetime.now().date():
        helpers.update_db()
    else:
        pass

    kpi = Case.get_kpi()
    return render_template('index.html',
                           active="home",
                           total_cases="{:,}".format(kpi[0]),
                           total_recovered="{:,}".format(kpi[1]),
                           total_deaths="{:,}".format(kpi[2]),
                           total_critical="{:,}".format(kpi[3]))


@app.route("/dashboard")
def dashboard():
    cases = Case.get_all_cases()
    cases = cases[['name', 'new_confirmed', 'all_confirmed', 'new_deaths', 'all_deaths', 'all_recovered', 'all_critical', 'population']]
    cases = cases.rename(columns={'name': 'Country',
                                  'all_confirmed': 'Total Cases',
                                  'new_confirmed': 'New Cases',
                                  'all_deaths': 'Total Deaths',
                                  'new_deaths': 'New Deaths',
                                  'all_recovered': 'Total Recovered',
                                  'all_critical': 'Total Critical',
                                  'population': 'Population'})

    return render_template('dashboard.html',
                           active="dashboard",
                           cases_data=cases.values.tolist(),
                           cases_colHeaders=cases.columns.tolist())


@app.route("/my_map")
def my_map():
    return render_template("my_map.html")


@app.route("/interactive_map")
def interactive_map():
    my_map = folium.Map(min_zoom=2, max_bounds=True, tiles='cartodbpositron')
    cases = Case.get_all_cases()

    sum_cases = sum(cases['all_confirmed'])
    for index, row in cases.iterrows():
        popup = '<b>{}</b><br><span style="color:gray;">Confirmed:{}</span><br>' \
                '<span style="color:red;">Deaths:{}</span><br>' \
                '<span style="color:green;">Recovered:{}</span>'.format(row['name'],
                                                                        "{:,}".format(row['all_confirmed']),
                                                                        "{:,}".format(row['all_deaths']),
                                                                        "{:,}".format(row['all_recovered']))
        folium.CircleMarker(
            location=[row['latitude'], row['longitude']],
            popup=popup,
            radius=(row['all_confirmed']/sum_cases)*300,
            color='crimson',
            fill=True,
            fill_color='crimson').add_to(my_map)

    parent_path = Path(os.path.abspath(os.path.dirname(__file__)))
    outfile = os.path.join(os.path.join(parent_path, 'templates'), 'my_map.html')
    my_map.save(outfile=outfile)

    last_updated_on = Case.get_last_update()
    return render_template("interactive_map.html", active="interactive_map", last_updated_on=last_updated_on)
