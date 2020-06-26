#!/usr/bin/python3
import pandas as pd
from bs4 import BeautifulSoup
import requests
import glob
import os
import Utilities
import numpy as np
import logging


def get_csv_files(folder):
    return glob.glob(folder)


def splitTickersBySectors(folder, logging):
    '''
    Remove all the rows where "Analyst Consensus" is unknown
    Create the folders structure
    Organize all the tickers by sector, and also Buy and Sell
            Sectors\Sector name\Buy --> folder
            Sectors\Sector name\Sell --> folder
            Sectors\Sector name\Sector name --> .csv file
            Sectors\Sector name\Sector nameBuy --> .csv file
            Sectors\Sector name\Sector nameSell --> .csv file
            downloadedData10mo\Buy --> To download the last 10 months of data
            downloadedData10mo\Sell --> To download the last 10 months of data
        AllStocks.csv --> File with all the stocks
    '''
    all_files = get_csv_files(folder + '\*.csv')
    li = []
    for filename in all_files:
        df = pd.read_csv(filename, header=0, usecols=['Ticker', 'Company Name', 'Analyst Consensus', 'Sector'])
        li.append(df)
    frame = pd.concat(li, axis=0, ignore_index=True)

    # part 2
    nan_value = float("NaN")
    frame.replace("", nan_value, inplace=True)
    frame.dropna(subset=["Analyst Consensus"], inplace=True)
    logging.info('NaN values deleted')

    frame.to_csv('AllStocks.csv')
    logging.info('All stocks available saved in: AllStocks.csv')
    sectors = frame['Sector'].unique()

    os.makedirs('downloadedData10mo\Buy', exist_ok=True)
    os.makedirs('downloadedData10mo\Sell', exist_ok=True)

    for sector in sectors:
        logging.info('Creating folders and splitting tickers for {} sector.'.format(sector))
        os.makedirs('Sectors\{}\Buy'.format(sector), exist_ok=True)
        os.makedirs('Sectors\{}\Sell'.format(sector), exist_ok=True)
        temp = frame.loc[frame.loc[:, 'Sector'] == sector]
        temp.to_csv('Sectors\{}\{}.csv'.format(sector, sector), header=0)
        tempBuy = temp[temp['Analyst Consensus'].str.contains('Buy')]
        tempSell = temp[temp['Analyst Consensus'].str.contains('Sell')]
        tempBuy.to_csv('Sectors\{}\{}Buy.csv'.format(sector, sector))
        tempSell.to_csv('Sectors\{}\{}Sell.csv'.format(sector, sector))


def combinations(logging):
    '''
       Create two files one for buys and other for sell for each sector.
       Each file contains the column 'Adj. Close' previous downloaded from yahoo.
       The files are saved in 'Buy' and 'Sell' folders for each sector
           Sectors\Sector name\Sector name_Buy.csv  -->file
           Sectors\Sector name\Sector name_Sell.csv  -->file
    '''
    listaDeSectores = get_csv_files("Sectors\*")
    # print(listaDeSectores)
    for sector in listaDeSectores:
        sec = sector.split('\\')[1]

        sell_files = glob.glob("Sectors\{}\Sell\*.csv".format(sec))
        buy_files = glob.glob("Sectors\{}\Buy\*.csv".format(sec))
        i = 0
        j = 0
        if len(sell_files) > 0 and len(buy_files) > 0:
            logging.info("For sector: {}: there are {} possible combinations, columns needed it {}.".format(sector.split('\\')[1],
                                                                                                              len(
                                                                                                                  sell_files) * len(
                                                                                                                  buy_files),
                                                                                                              2 * (len(
                                                                                                                  sell_files) * len(
                                                                                                                  buy_files))))
            ##################################
            ##################################
            #########    Sell    #############
            ##################################
            listaSell = []
            listaSell_tickers = []
            for file in sell_files:
                frame = pd.read_csv(file, usecols=['Adj Close'])
                activo = sell_files[i].split('\\')[-1].split('.')[0]
                listaSell_tickers.append(activo)
                frame.rename(columns={"Adj Close": "{}".format(os.path.splitext(os.path.basename(file))[0])},
                             inplace=True)
                listaSell.append(frame)
                i += 1

            sellss = pd.concat(listaSell, axis=1, ignore_index=True)
            sellss.columns = listaSell_tickers
            sellss[:61].to_csv('Sectors\{}\{}_Sells.csv'.format(sec, sec))
            logging.info("File saved in: Sectors\{}\{}_Sells.csv".format(sec, sec))


            ##################################
            ##################################
            #########    Buys    #############
            ##################################
            listaBuy = []
            listaBuy_tickers = []

            for file in buy_files:
                frame = pd.read_csv(file, usecols=['Adj Close'])
                activo = buy_files[j].split('\\')[-1].split('.')[0]
                listaBuy_tickers.append(activo)
                frame.rename(columns={"Adj Close": "{}".format(os.path.splitext(os.path.basename(file))[0])},
                             inplace=True)
                listaBuy.append(frame)
                j += 1

            buyeerss = pd.concat(listaBuy, axis=1, ignore_index=True)
            buyeerss.columns = listaBuy_tickers
            # print(buyeerss)
            buyeerss[:61].to_csv('Sectors\{}\{}_Buys.csv'.format(sec, sec))
            logging.info("File saved in: Sectors\{}\{}_Buys.csv".format(sec, sec))



def performance(logging):
    '''
       Divide the column 'Adj. Close' of each ticker Buy/Sell in order to get the performance
       It does all the combination (on each sector).
       Once all the combinations are done and saved: Totales_Sector name.csv
       Then reduce all this numbers to one, finding the equation of the line with this dots.
       As big the number is, the profits would be higher.
           Sectors\Sector name\Totales Sector name.csv  --> file with all the combinations Buy/Sell
           Sectors\Sector name\Resultados Sector name.csv  --> file with the final result
    '''
    listaDeSectores = glob.glob("Sectors\*")

    for sector in listaDeSectores:
        sec = sector.split('\\')[1]
        logging.info("Processing {} sector...".format(sec))
        ficheros = glob.glob('Sectors\{}\*'.format(sec))
        for file in ficheros:
            if len(file.split('_Buys.csv')) > 1:
                buyeerss = pd.read_csv(file, index_col=0)
            if len(file.split('_Sells.csv')) > 1:
                sellss = pd.read_csv(file, index_col=0)

        listaResultadosPandas = []
        listaResultadosNombreColumnas = []

        for i in range(0, len(buyeerss.count(axis=0))):
            for j in range(0, len(sellss.count(axis=0))):
                calculo = buyeerss.iloc[:, i] / sellss.iloc[:, j]
                listaResultadosPandas.append(calculo)
                tempB = buyeerss.columns[i]
                tempS = sellss.columns[j]
                listaResultadosNombreColumnas.append(tempB + "-" + tempS)

        resultadosTotales = pd.concat(listaResultadosPandas, axis=1, ignore_index=True)
        resultadosTotales.columns = listaResultadosNombreColumnas
        logging.info("Saving all the combinations possible Long\Short in: Sectors\{}\Totales_{}.csv".format(sec, sec))
        resultadosTotales.to_csv('Sectors\{}\Totales_{}.csv'.format(sec, sec))

        slopes = resultadosTotales.apply(lambda x: np.polyfit(resultadosTotales.index, x, 1)[0])
        # print(slopes)
        slopes.columns = ['Long-Short', 'Ratio']
        slopes.to_csv('Sectors\{}\Resultados_{}.csv'.format(sec, sec))
        temp = pd.read_csv('Sectors\{}\Resultados_{}.csv'.format(sec, sec))
        temp.rename({'Unnamed: 0': 'Long-Short', '0': 'Ratio'}, inplace=True, axis=1)
        temp['Sector'] = sec
        temp.to_csv('Sectors\{}\Resultados_{}.csv'.format(sec, sec))
        logging.info("Saving the ratios from all the combinations possible in: Sectors\{}\Resultados_{}.csv".format(sec, sec))


def selecting_tops(logging, qty, repeated):

    listaDeSectores = glob.glob("Sectors\*")
    listaResultados = []

    for sector in listaDeSectores:
        sec = sector.split('\\')[1]

        ficheros = glob.glob('Sectors\{}\*'.format(sec))
        for file in ficheros:
            if 'Resultados_' in file:
                resultadosFrame = pd.read_csv(file, index_col=0)
                listaResultados.append(resultadosFrame)

    frame = pd.concat(listaResultados, axis=0, ignore_index=False)
    frame.sort_values(by=['Ratio'], ascending=False, inplace=True)

    frame.to_csv('AllPosibleRatios.csv')
    logging.info("All the sector ratios are sorted and saved in: AllPosibleRatios.csv")
    if repeated == False:
        tickersPosNoRepeated = Utilities.getPortfolioNoNRepeated(qty, frame['Long-Short'].tolist())
        frame.iloc[tickersPosNoRepeated, :].to_csv('Top_{}_Ratios.csv'.format(qty))
        logging.info("The top {} ratios NO REPEATING ticker file is located in: Top_{}_Ratios.csv".format(qty, qty))
    else:
        frame.head(qty).to_csv('Top_{}_Ratios.csv'.format(qty))
        logging.info("The top {} ratios ticker file is located in: Top_{}_Ratios.csv".format(qty, qty))

