import requests
import csv
import pandas as pd
import json

# TODO impliment region selection from command line either by numbered choice
#      or by case insensitive match using regions.csv for region number
# TODO extract names as well from typeids.csv for personal sanity
# TODO decide on if we want to manage data visualization either using spreadsheet
#      functions or with python data visualization (numpy)
# TODO figure out how to grab the data we want out of the JSON
#           Looking Quantity sold of owned bp items and at what price
#           Look for ROI in just buyin mats in region to manufacture


def getdata():
    """This Function Grabs the Data from the API and puts it into a json file
    for later manipulation so not to overload the API with redundant requests
    at the moment this fucntion queries an unknown region or maybe total market
    data for the last 24 hours. The api supports a regionid and a time frame
    unsure how to impliment that as of yet."""

    print("Refreshing Data... Please Wait")
    ids = ""
    data = [row for row in csv.reader(open("typeids.csv"))]
    for item in data:
        ids += "," + item[0]
    r = requests.get(
        "https://api.evemarketer.com/ec/marketstat/json?typeid=" + ids.lstrip(",")
    )
    with open("marketdata.json", "w") as f:
        f.write(r.text)


TYPEID = "typeId"


def queryJSON():
    types = {}
    with open("typeids.csv", "r") as typeFile:
        typeCSV = csv.DictReader(typeFile)
        for line in typeCSV:
            types[line[TYPEID]] = line["Name"]

    with open("marketdata.json", "r") as jsonFile:
        data = json.load(jsonFile)

    # setup column names
    orderTypes = ["buy", "sell"]
    attributes = ["avg", "fivePercent", "max", "median", "min", "stdDev", "variance", "volume", "wavg"]
    columns = ["typeId", "itemName"]
    for order in orderTypes:
        for attribute in attributes:
            columns.append(order + attribute)

    # process json into nested lists
    newData = []
    for row in data:
        typeId = row['buy']['forQuery']['types'][0]
        newRow = [typeId, types[str(typeId)]]
        for order in orderTypes:
            for attribute in attributes:
                newRow.append(row[order][attribute])
        newData.append(newRow)

    # create pandas dataframe from nested lists
    df = pd.DataFrame(newData, columns=columns)
    return df


if __name__ == "__main__":
    queryJSON()
    # refresh = input("Would you like to refresh market data with new information? y/n")
    # if refresh == 'y':
    #    getdata()

    # else:
    #    print("Goodbye Noob")
