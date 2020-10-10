from uk_covid19 import Cov19API
import json, seaborn, numpy, pandas, matplotlib.pyplot as plt, matplotlib.dates as mdates

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
        day["date"] = mdates.datestr2num(day["date"])

    return pandas.DataFrame(data)

seaborn.set_theme(style="darkgrid")
data = parse_data(get_data_from_api())
data = data.sort_values("date")

fig, ax = plt.subplots()

# seaborn.barplot(x=data["date"], y=data["dailyCasesAsPercTests"], ax=ax)
# seaborn.lineplot(x=data["date"], y=data["cumCasesAsPercTests"], ax=ax)

ax.bar(data["date"], data["dailyCasesAsPercTests"], color="lightblue")
ax.plot(data["date"], data["cumCasesAsPercTests"], color="red")

locator = mdates.AutoDateLocator()
formatter = mdates.ConciseDateFormatter(locator)
ax.xaxis.set_major_locator(locator)
ax.xaxis.set_major_formatter(formatter)

plt.ylabel("Percentage of COVID-19 cases found positive")
plt.xlabel("Date")
ax.set_title("Daily and Cumulative percentage of UK COVID-19 cases found positive")

plt.show()