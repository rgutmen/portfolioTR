#!/usr/bin/python3

import pandas as pd
from bs4 import BeautifulSoup
import requests
from datetime import datetime
from dateutil.relativedelta import relativedelta
import time
import glob
import pathlib
import Utilities


def getTotalToDownload(fileList):
    lista = []
    for filename in fileList:
        df = pd.read_csv(filename, header=0, usecols=['Ticker', 'Company Name', 'Analyst Consensus', 'Sector'])
        lista.append(df)
    frame = pd.concat(lista, axis=0, ignore_index=True)
    return len(frame)


def getYahoo5yoData(logging, downloadsLog):
    '''
     Download the 5years data from yahoo finance
     Only save the file if the ticker has 5 years data old to avoid new instruments with no enough data
     The files are saved in 'Buy' and 'Sell' folders for each sector
         Sectors\Sector name\Buy
         Sectors\Sector name\Sell
     '''
    # pat = os.getcwd()
    # filesBuy = glob.glob('Sectors\**\*Buy.csv'.format(pat), recursive=True)
    # filesSell = glob.glob('Sectors\**\*Sell.csv'.format(pat), recursive=True)
    filesBuy = glob.glob('Sectors\**\*Buy.csv', recursive=True)
    filesSell = glob.glob('Sectors\**\*Sell.csv', recursive=True)

    time_now = datetime.now() - relativedelta(days=2)
    five_yrs_ago = time_now - relativedelta(years=5, months=1)
    time_now_unix = int(time.mktime(time_now.timetuple()))
    five_yrs_ago_unix = int(time.mktime(five_yrs_ago.timetuple()))

    logging.info('Downloading 5 years data for each ticker.')
    lenFilesBuy = getTotalToDownload(filesBuy)
    lenFilesSell = getTotalToDownload(filesSell)

    logging.info('Downloading {} tickers with option to Buy.'.format(lenFilesBuy))
    downloadsLog.info('Downloading {} tickers with option to Buy.'.format(lenFilesBuy))

    for file in filesBuy:
        sector = pathlib.PurePath(file).parent.name
        df = pd.read_csv(file, usecols=['Ticker'])
        tickerList = df['Ticker'].to_list()
        for item in tickerList:
            if item == 'BRK.B':
                item = 'BRKB'
            try:
                url = "https://query1.finance.yahoo.com/v7/finance/download/{}?period1={}&period2={}&interval=1mo&events=history".format(
                    item, five_yrs_ago_unix, time_now_unix)
                data = pd.read_csv(url)
                if (len(data)) > 60:
                    data.to_csv('Sectors\{}\Buy\{}.csv'.format(sector, item))
                    downloadsLog.info('Data downloaded and saved in: Sectors\{}\Buy\{}.csv'.format(sector, item))
                else:
                    logging.warning("Data for {} doesn't have 5 years old.".format(item))
                    downloadsLog.warning("Data for {} doesn't have 5 years old.".format(item))
            except:
                logging.error(
                    "It wasn't possible get the data for {}, from: {}. Please, check manually".format(item, url))
                downloadsLog.error(
                    "It wasn't possible get the data for {}, from: {}. Please, check manually".format(item, url))

    logging.info('Downloading {} tickers with option to Sell.'.format(lenFilesSell))
    downloadsLog.info('Downloading {} tickers with option to Sell.'.format(lenFilesSell))
    for file in filesSell:
        sector = pathlib.PurePath(file).parent.name
        df = pd.read_csv(file, usecols=['Ticker'])
        tickerList = df['Ticker'].to_list()
        for item in tickerList:
            if item == 'BRK.B':
                item = 'BRKB'
            try:
                url = "https://query1.finance.yahoo.com/v7/finance/download/{}?period1={}&period2={}&interval=1mo&events=history".format(
                    item, five_yrs_ago_unix, time_now_unix)
                data = pd.read_csv(url)
                if (len(data)) > 60:
                    data.to_csv('Sectors\{}\Sell\{}.csv'.format(sector, item))
                    downloadsLog.info('Data downloaded and saved in: Sectors\{}\Sell\{}.csv'.format(sector, item))
                else:
                    logging.warning("Data for {} doesn't have 5 years old.".format(item))
                    downloadsLog.warning("Data for {} doesn't have 5 years old.".format(item))
            except:
                logging.error(
                    "It wasn't possible get the data for {}, from: {}. Please, check manually".format(item, url))
                downloadsLog.error(
                    "It wasn't possible get the data for {}, from: {}. Please, check manually".format(item, url))


def getBetasAnd10mData(logging, downloadsLog, qty):
    df = pd.read_csv('Top_{}_Ratios.csv'.format(qty))

    pairs = df['Long-Short'].tolist()
    allSectors = pd.read_csv('AllStocks.csv')
    betasList = []
    sectorsList = []
    tickerToDownload, shortTickers = Utilities.getNamesNoNRepeated(pairs)

    time_now = datetime.now() - relativedelta(days=1)
    eleven_mon_ago = time_now - relativedelta(months=10)
    time_now_unix = int(time.mktime(time_now.timetuple()))
    elev_mon_ago_unix = int(time.mktime(eleven_mon_ago.timetuple()))
    count = 0
    logging.info('Downloading betas')
    for i in range(0, len(tickerToDownload)):

        url = 'https://finance.yahoo.com/quote/{}'.format(tickerToDownload[i])
        try:
            html_content = requests.get(url).text

        except requests.exceptions.InvalidSchema as e:
            logging.error("Url error for {} : {}, please, check manually.".format(tickerToDownload[i], e))
            downloadsLog.error("Url error for {} : {}, please, check manually.".format(tickerToDownload[i], e))
        try:
            soup = BeautifulSoup(html_content, "lxml")
            contentTable = soup.find('td', {"data-test": "BETA_5Y-value"})
            betasList.append(float(contentTable.text))
            sectorsList.append(allSectors.loc[allSectors['Ticker'] == tickerToDownload[i]].Sector.values[0])
        except UnboundLocalError:
            logging.error("It wasn't possible to get the beta for the ticker: {}, please, check manually.".format(
                tickerToDownload[i], url))
            downloadsLog.error("It wasn't possible to get the beta for the ticker: {}, please, check manually.".format(
                tickerToDownload[i], url))

        url = "https://query1.finance.yahoo.com/v7/finance/download/{}?period1={}&period2={}&interval=1mo&events=history".format(
            tickerToDownload[i], elev_mon_ago_unix, time_now_unix)
        try:
            data = pd.read_csv(url)
        except FileNotFoundError:
            logging.error(
                "It wasn't possible to get the 10 months data for ticker: {}, please, check manually.".format(
                    tickerToDownload[i], url))
            downloadsLog.error(
                "It wasn't possible to get the 10 months data for ticker: {}, please, check manually.".format(
                    tickerToDownload[i], url))

        if tickerToDownload[i] in shortTickers:
            try:
                data.to_csv('downloadedData10mo\Sell\{}.csv'.format(tickerToDownload[i]))
                logging.info("Ticker: {}. Saved in: downloadedData10mo\Sell\{}.csv".format(tickerToDownload[i],
                                                                                           tickerToDownload[i]))
                downloadsLog.info("Ticker: {}. Saved in: downloadedData10mo\Sell\{}.csv".format(tickerToDownload[i],
                                                                                                tickerToDownload[i]))
            except UnboundLocalError:
                logging.error(
                    "It wasn't possible to save the 10 months data for ticker: {}, in: downloadedData10mo\Sell\{}.csv.".format(
                        tickerToDownload[i], tickerToDownload[i]))
                downloadsLog.error(
                    "It wasn't possible to save the 10 months data for ticker: {}, in: downloadedData10mo\Sell\{}.csv.".format(
                        tickerToDownload[i], tickerToDownload[i]))
        else:
            try:
                data.to_csv('downloadedData10mo\Buy\{}.csv'.format(tickerToDownload[i]))
                logging.info("Ticker: {}. Saved in: downloadedData10mo\Buy\{}.csv".format(tickerToDownload[i],
                                                                                          tickerToDownload[i]))
                downloadsLog.info("Ticker: {}. Saved in: downloadedData10mo\Buy\{}.csv".format(tickerToDownload[i],
                                                                                               tickerToDownload[i]))
            except UnboundLocalError:
                logging.error(
                    "It wasn't possible to save the 10 months data for ticker: {}, in: downloadedData10mo\Sell\{}.csv.".format(
                        tickerToDownload[i], tickerToDownload[i]))
                downloadsLog.error(
                    "It wasn't possible to save the 10 months data for ticker: {}, in: downloadedData10mo\Sell\{}.csv.".format(
                        tickerToDownload[i], tickerToDownload[i]))

    dictio = {
        'Ticker': tickerToDownload,
        'Beta': betasList,
        'Sector': sectorsList
    }

    df = pd.DataFrame(dictio)  # , columns=['Ticker', 'Beta', 'Sector'])
    # df = pd.DataFrame(dictio.items())#, columns=['Ticker', 'Beta', 'Sector'])
    df.to_csv('Betas.csv')
