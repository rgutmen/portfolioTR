import pandas as pd
from itertools import chain


def boolean_string(s):
    if s not in {'False', 'True'}:
        raise ValueError('Not a valid boolean string')
    return s == 'True'


def makeMaths(df):
    df = makeHL(df)
    df = makeATR(df)
    df = makeATRP(df)
    return df


def makeATR(df):
    highList = df['High'].tolist()
    lowList = df['Low'].tolist()
    ycList = df['Close'].tolist()
    # print(ycList)
    ycList = ycList[1:]
    # print(ycList)
    atrList = []
    for x in reversed(range(len(highList))):
        tempList = []
        # Today's high minus today's low
        tempList.append(highList[x] - lowList[x])
        # The absolute value of today's high minus yesterday's close
        tempList.append(abs(highList[x] - ycList[x - 1]))
        # The absolute value of today's low minus yesterday's close
        tempList.append(abs(lowList[x] - ycList[x - 1]))

        atrList.append(max(tempList))
    atrList[len(atrList) - 1] = highList[len(atrList) - 1] - lowList[len(atrList) - 1]
    atrList.reverse()
    df['ATR'] = atrList
    return df


def getPortfolioNoNRepeated(qtyRequired, allTickersList):
    results = []
    buyersList = []
    sellersList = []
    for i in range(0, len(allTickersList)):
        if (allTickersList[i].split('-')[0] not in buyersList) and (allTickersList[i].split('-')[1] not in sellersList):
            results.append(i)
            buyersList.append(allTickersList[i].split('-')[0])
            sellersList.append(allTickersList[i].split('-')[1])
        if len(results) == qtyRequired:
            break

    return results


def getNamesNoNRepeated(pairs):
    results = []
    shortTickers = []
    for item in pairs:
        results.append(item.split('-')[0])
        results.append(item.split('-')[1])
        shortTickers.append(item.split('-')[1])

    return list(set(results)), shortTickers


def getBetaFromFile(name):
    df = pd.read_csv('Betas.csv')
    return df['Beta'][df['Ticker'] == name]


def makeHL(df):
    df['HL'] = df['High'] - df['Low']
    return df


def makeATRP(df):
    df['ATRP'] = (df['ATR'] / df['Close'])
    return df


def unNestList(listTemp):
    return list(chain.from_iterable(listTemp))


def getTickersToTrade(qty):
    temp = pd.read_csv('Top_{}_Ratios.csv'.format(qty), usecols=['Long-Short', 'Sector']).values.tolist()
    return temp
