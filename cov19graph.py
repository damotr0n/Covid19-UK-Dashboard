from uk_covid19 import Cov19API
import json, seaborn, numpy, pandas, matplotlib.pyplot as plt

# Fetches the data from the api
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
    return api.get_json()


# Computes the data that I am interested in
# And gets rid of any incompatible data
# Returns an ndarray
def parse_data(input_data):

    data = [day for day in input_data["data"] if day["dailyTests"] != None]

    for day in data:
        day["dailyCasesAsPercTests"] = (day["dailyCases"] / day["dailyTests"]) * 100
        day["cumCasesAsPercTests"] = (day["cumCases"] / day["cumTests"]) * 100
        del day["dailyCases"]
        del day["cumCases"]
        del day["dailyTests"]
        del day["cumTests"]

    # return numpy.array(proc_data)
    return pandas.DataFrame(data)

seaborn.set_theme(style="darkgrid")
data = parse_data(get_data_from_api())
plot = seaborn.relplot(data=data, x="date", y="dailyCasesAsPercTests",  kind="line")
plot.fig.autofmt_xdate()

plt.show()