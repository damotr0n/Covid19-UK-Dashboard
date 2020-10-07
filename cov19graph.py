from uk_covid19 import Cov19API
import json


def get_data_from_api():

    # Filter
    all_uk_data = [
        'areaType=overview'
    ]

    # Structure
    cases_and_tests = {
        "date": "date",
        "dailyCases": "newCasesByPublishDate",
        "cumCases": "cumCasesByPublishDate",
        "dailyTests": "newTestsByPublishDate",
        "cumTests": "cumTestsByPublishDate"
    }

    api = Cov19API(all_uk_data, cases_and_tests)

    data = api.get_json()

    print(json.dumps(data, indent=4))


get_data_from_api()

