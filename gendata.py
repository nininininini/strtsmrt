import csv
import datetime
import sentiment
import sys

csv.field_size_limit(sys.maxint)

def getStockData(symbol, date):
    file = open('data/hsd/' + symbol + '.csv')
    csv_file = csv.reader(file)

    # Get stock data for the next day
    date += datetime.timedelta(days=1)

    data = []

    print "Getting stock data for " + symbol + " for " + date.strftime('%Y-%m-%d')

    for row in csv_file:
        if(row[0] == date.strftime('%Y-%m-%d')):
            data.append(float(row[1]))
            data.append(float(row[4]))
            return data

    # No data found for symbol for given date
    return -1

def genData():
    data_file = open('data/dat.csv', 'w+')
    csv_writer = csv.writer(data_file)
    date = datetime.date(2013, 1, 1)
    endDate = datetime.date(2013, 6, 30)

    while(date <= endDate):
        print "Checking data for " + date.strftime('%Y-%m-%d')

        day = date.weekday()
        if(day == 4 or day == 5):
            date += datetime.timedelta(days=1)
            continue

        fname = date.strftime('%Y-%m-%d')
        file = open('data/news/' + fname + '.csv')
        csv_file = csv.reader(file)

        for row in csv_file:
            stockdata = getStockData(row[0], date)
            if(stockdata == -1):
                continue
            sentdata = sentiment.analyzeText(row[1])

            data = []
            data.extend((row[0], date.timetuple().tm_yday))
            data.extend((sentdata['probability']['neg'], sentdata['probability']['neutral'], sentdata['probability']['pos']))
            data.append(sentdata['label'])
            data.extend(stockdata)
            csv_writer.writerow(data)

        date += datetime.timedelta(days=1)

genData()
