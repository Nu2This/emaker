import requests
import csv


def getdata():
    print("Refreshing Data... Please Wait")
    ids = ''
    data = [row for row in csv.reader(open('typeids.csv'))]
    for item in data:
        ids += ',' + item[0]
    r = requests.get('https://api.evemarketer.com/ec/marketstat?typeid=' + ids.lstrip(','))
    with open('marketdata.xml', 'w') as f:
        f.write(r.text)


if __name__ == '__main__':
    refresh = input("Would you like to refresh market data with new information? y/n")
    if refresh == 'y':
        getdata()

    else:
        print("Goodbye Noob")
