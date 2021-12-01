from datetime import date, timedelta

import requests


class SearchId:

    def __init__(self, year, month, day, delta):
        self.year = year
        self.month = month
        self.day = day
        self.delta = delta

    def get_datas(self):
        date_from = date(self.year, self.month, self.day)
        date_stop = date_from + timedelta(self.delta)
        return date_from, date_stop

    def format_search_body(self) -> str:
        date_from, date_stop = SearchId.get_datas(self)
        search_body = """{
          "search_params": {
            "directions": [
              {
                "origin": "MSQ",
                "destination": "ZNZ",
                "date": """ + '"' + f"{date_from}" + '"'"""
              },
              {
                "origin": "ZNZ",
                "destination": "MSQ",
                "date": """ + '"' + f"{date_stop}" + '"'"""
              }
            ],
            "passengers": {
              "adults": 1,
              "children": 0,
              "infants": 0
            },
            "trip_class": "Y"
          },
          "client_features": {
            "direct_flights": true,
            "brand_ticket": true,
            "top_filters": true,
            "badges": true,
            "tour_tickets": true,
            "assisted": true,
            "credit_partner": true
          },
          "marker": "direct",
          "market_code": "by",
          "currency_code": "byn",
          "languages": {
            "ru": 1
          },
          "debug": {
            "experiment_groups": {
              "asb-exp-footerButton": "off",
              "asb-exp-ticketsVersion": "v2",
              "asb-exp-insurance": "separate",
              "asb-exp-feedback": "form",
              "avs-exp-aa": "on",
              "asb-exp-insuranceRedesign": "old",
              "prem-exp-webFloatingElement": "mysterious"
            }
          }
        }"""
        return search_body

    def get_search_id(self) -> str:
        search_body = SearchId.format_search_body(self)
        r = requests.post('https://www.aviasales.by/search-api/search/v2/start', data=search_body)
        response_json = r.json()
        search_id = response_json["search_id"]
        return search_id

