import requests
import csv
import xml.etree.ElementTree as ET
import pandas as pd
import json
from EveItemList import EvEItemList

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
        "https://api.evemarketer.com/ec/marketstat?typeid=" + ids.lstrip(",")
    )
    with open("marketdata.json", "w") as f:
        f.write(r.text)


TYPEID = "typeId"


def queryJSON():
<<<<<<< HEAD
    tree = ET.parse('marketdata.json')
    root = tree.getroot()
    child = root[0]
    items = child[0]
    for entry in items:
        print(entry[1])
    # data = []
    # cols = []
    #for i in range(len(root.getchildren())):
    #    child = root.getchildren()[i]
    #    data.append([subchild.text for subchild in child.getchildren()])
    #    cols.append(child.tag)

    #df = pd.DataFrame(data).T
    #df.columns = cols
    #print(df)
=======
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
    df.to_csv('clobbered.csv')
    return df


def processInventory(interestedItemIds):
    # https://www.fuzzwork.co.uk/dump/latest/

    types = {}
    with open('invTypes.csv', 'r', errors='replace') as typeFile:
        typeCSV = csv.DictReader(typeFile)
        for line in typeCSV:
            try:
                types[line["typeID"]] = line["typeName"]
            except:
                continue

    materialMapping = {}
    with open('invTypeMaterials.csv', 'r') as requirementsFile:
        requirementsCSV = csv.DictReader(requirementsFile)
        for line in requirementsCSV:
            if line["typeID"] in materialMapping.keys():
                materialMapping[line["typeID"]].append((line["materialTypeID"], line["quantity"], types[line["materialTypeID"]]))
            else:
                materialMapping[line["typeID"]] = [(line["materialTypeID"], line["quantity"], types[line["materialTypeID"]])]

    itemMapping = EvEItemList(types, materialMapping)
    itemMapping.CalculateAllRawMaterials()
    return itemMapping
>>>>>>> ethan


if __name__ == "__main__":
    processInventory([])
    queryJSON()
    # refresh = input("Would you like to refresh market data with new information? y/n")
    # if refresh == 'y':
    #    getdata()

    # else:
    #    print("Goodbye Noob")
