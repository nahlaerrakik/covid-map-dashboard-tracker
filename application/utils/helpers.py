__author__ = 'nahla.errakik'

import datetime
from geopy.geocoders import Nominatim
from application.utils.api import CovidAPI
from application.models import Country, Case


def insert_db():
    data = CovidAPI().get_data()
    for item in data:
        country = set_country(item)
        if country is not None:
            country.insert()

            case = Case(country=item['code'],
                        new_confirmed=item['today']['confirmed'],
                        new_deaths=item['today']['deaths'],
                        all_confirmed=item['latest_data']['confirmed'],
                        all_deaths=item['latest_data']['deaths'],
                        all_recovered=item['latest_data']['recovered'],
                        all_critical=item['latest_data']['critical'],
                        last_updated_at=datetime.datetime.strptime(item['updated_at'], '%Y-%m-%dT%H:%M:%S.%fZ'))
            case.insert()


def update_db():
    data = CovidAPI().get_data()
    for item in data:
        case = Case(country=item['code'],
                    new_confirmed=item['today']['confirmed'],
                    new_deaths=item['today']['deaths'],
                    all_confirmed=item['latest_data']['confirmed'],
                    all_deaths=item['latest_data']['deaths'],
                    all_recovered=item['latest_data']['recovered'],
                    all_critical=item['latest_data']['critical'],
                    last_updated_at=datetime.datetime.strptime(item['updated_at'], '%Y-%m-%dT%H:%M:%S.%fZ'))
        is_updated = case.update()

        if not is_updated:
            country = set_country(item)
            if country is not None:
                country.insert()
                case.insert()


def set_country(item):
    if item['latest_data']['confirmed'] <= 0:
        return None

    latitude = item['coordinates']['latitude']
    longitude = item['coordinates']['longitude']
    if latitude in [None, 0] or longitude in [None, 0]:
        coordinates = get_coordinates(item['name'])
        if coordinates is not None:
            latitude = coordinates.latitude
            longitude = coordinates.longitude
        else:
            latitude = 0
            longitude = 0

    country = Country(id=item['code'],
                      name=item['name'],
                      latitude=latitude,
                      longitude=longitude,
                      population=item['population'])

    return country


def get_coordinates(address):
    geo_locator = Nominatim(user_agent='covid-map-application')
    location = geo_locator.geocode(address)

    return location
