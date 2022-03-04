import requests
import csv


def getdata(ids):
    print("Refreshing Data... Please Wait")
    r = requests.get('https://api.evemarketer.com/ec/marketstat?typeid=' + ids.lstrip(','))
    with open('marketdata.xml', 'w') as f:
        f.write(r.text)


def readcsv():
    out = ''
    data = [row for row in csv.reader(open('/mnt/c/Users/Mike/Documents/'\
            'Python/eve/typeids.csv'))]
    for item in data:
        out += ',' + item[0]
    return out


if __name__ == '__main__':
    refresh = input("Would you like to refresh market data with new information? y/n")
    if refresh == 'y':
        getdata(readcsv())

    else:
        print("Goodbye Noob")
