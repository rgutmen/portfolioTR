#!/usr/bin/python3
import argparse
import logging
import logMaker
import processFoldersData
import downloadData
import Utilities
import excelCreator

import os
import shutil

parser = argparse.ArgumentParser(description='Hace un portfolio con activos de etoro.')
parser.add_argument('folder', type=str, help='Folder where are the files from TipRanks')
parser.add_argument('qty', type=int, default=10, help='Amount of tickers required.')
parser.add_argument('rptd', type=Utilities.boolean_string, default=False, help='repeated values.')
args = parser.parse_args()

if __name__ == '__main__':

    # if os.path.isdir('Sectors'):
    #     shutil.rmtree('Sectors')
    # if os.path.isdir('downloadedData10mo'):
    #     shutil.rmtree('downloadedData10mo')
    # if os.path.isfile('Top_20_Ratios_R.csv'):
    #     os.remove('Top_20_Ratios_R.csv')
    # if os.path.isfile('Betas.csv'):
    #     os.remove('Betas.csv')
    # if os.path.isfile('app.log'):
    #     os.remove('app.log')
    # if os.path.isfile('AllPosibleRatios.csv'):
    #     os.remove('AllPosibleRatios.csv')
    # if os.path.isfile('AllStocks.csv'):
    #     os.remove('AllStocks.csv')
    # if os.path.isfile('appDownloads.log'):
    #     os.remove('appDownloads.log')


    logger = logMaker.setup_logger('main_app', 'app.log')
    loggerDownloads = logMaker.setup_logger('downloads_logger', 'appDownloads.log')
    logger.info('Parameters used: {} {} {}'.format(args.folder, args.qty, args.rptd))

    logging.info('Starting Program')
    processFoldersData.splitTickersBySectors(args.folder, logger)
    downloadData.getYahoo5yoData(logger, loggerDownloads)
    processFoldersData.combinations(logger)
    processFoldersData.performance(logger)
    processFoldersData.selecting_tops(logger, args.qty, args.rptd)
    downloadData.getBetasAnd10mData(logger, loggerDownloads, args.qty)
    excelCreator.makingExcel(logger, args.qty)


