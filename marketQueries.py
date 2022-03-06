import requests
import csv
import json


def getdata():
    print("Refreshing Data... Please Wait")
    ids = ''
    data = [row for row in csv.reader(open('typeids.csv'))]
    for item in data:
        ids += ',' + item[0]
    r = requests.get('https://api.evemarketer.com/ec/marketstat/json?typeid=' + ids.lstrip(','))
    with open('marketdata.json', 'w') as f:
        f.write(r.text)
def queryJSON():
    with open('marketdata.json') as json_file:
        data = json.load(json_file)

if __name__ == '__main__':
    queryJSON()
    #refresh = input("Would you like to refresh market data with new information? y/n")
    #if refresh == 'y':
    #    getdata()

    #else:
    #    print("Goodbye Noob")
