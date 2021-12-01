import string
from datetime import datetime
import random

import requests

from aviasales_holidays.aviasales_search_id import SearchId


class Prise(SearchId):

    def id_generator(self, size=5, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    def format_search_body_prise(self) -> str:
        query_search_id = SearchId.get_search_id(self)
        timestamp = datetime.timestamp(datetime.now())
        body = """{
            "search_id": """ + '"' + f"{query_search_id}" + '"' + """,
            "rnd": """ + '"' + f"{Prise.id_generator(self)}" + '"' + """,
            "last_update_timestamp": """ + f"{int(timestamp)}" + """,
            "brand_ticket_agent_ids": [],
            "required_tickets": [],
            "limit": 10,
            "filters": {},
            "order": "best"
        }"""
        return body

    def get_prise(self) -> str:
        response_json = []
        while not response_json:
            search_body = Prise.format_search_body_prise(self)
            r = requests.post('https://www.aviasales.by/search-api/search/v3/results', data=search_body)
            print(r.status_code)
            if r.status_code == 304:
                continue
            response_json = r.json()
        list_of_costs = []
        for j in response_json[0]["tickets"]:
            for m in j["proposals"]:
                list_of_costs.append(m["price"]["value"])
        lowest_cost = min(list_of_costs)
        date_from, date_stop = SearchId.get_datas(self)
        response = f"""
START DATE: {date_from} 
END DATE: {date_stop} 
Lowest Coast - {int(lowest_cost)} BYN"""
        print(response)
        return response

