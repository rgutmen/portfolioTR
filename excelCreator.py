import xlsxwriter
import pandas as pd
import Utilities


def makingExcel(logging, qty):
    tickersList = Utilities.getTickersToTrade(qty)
    # print(tickersList)

    for item in tickersList:
        longTicker = item[0].split('-')[0]
        shortTicker = item[0].split('-')[1]
        sector = item[1]

        acL = pd.read_csv('downloadedData10mo\Buy\{}.csv'.format(longTicker), parse_dates=['Date'])
        acS = pd.read_csv('downloadedData10mo\Sell\{}.csv'.format(shortTicker), parse_dates=['Date'])
        acLCompleted = Utilities.makeMaths(acL)
        acSCompleted = Utilities.makeMaths(acS)
        acLCompleted['Date'] = acLCompleted['Date'].dt.strftime('%d/%m/%Y')
        acSCompleted['Date'] = acSCompleted['Date'].dt.strftime('%d/%m/%Y')

        adcLL = pd.read_csv('Sectors\{}\Buy\{}.csv'.format(sector, longTicker), parse_dates=['Date'])
        adcLL['Date'] = adcLL['Date'].dt.strftime('%d/%m/%Y')
        adcSL = pd.read_csv('Sectors\{}\Sell\{}.csv'.format(sector, shortTicker), parse_dates=['Date'])

        spreads = pd.read_csv('Sectors\{}\Totales_{}.csv'.format(sector, sector))
        allRatios = pd.read_csv('Sectors\{}\Resultados_{}.csv'.format(sector, sector), index_col=0)
        ratio = allRatios[allRatios['Long-Short'] == '{}-{}'.format(longTicker, shortTicker)].Ratio.values.item()

        if (len(acL) == len(acS)) and (len(adcLL) == len(adcSL)):
            workbook = xlsxwriter.Workbook('{}-{}.xlsx'.format(longTicker, shortTicker))
            worksheet_ratio = workbook.add_worksheet('Ratio')
            worksheet_spread = workbook.add_worksheet('Spread')
            logging.info("Creating {}-{} spreadsheet.".format(longTicker, shortTicker))
            # Formatters
            date_format_long = workbook.add_format({'num_format': 'd/m/yyyy', 'bg_color': '#33CC33'})
            date_format_short = workbook.add_format({'num_format': 'd/m/yyyy', 'bg_color': '#FF3D01'})
            date_format = workbook.add_format({'num_format': 'd/m/yyyy'})
            bold = workbook.add_format({'bold': True})
            greenbg_bold = workbook.add_format({'bold': True, 'bg_color': '#33CC33', 'align': 'center'})
            ocrebg_bold = workbook.add_format({'bold': True, 'bg_color': '#C4BD97', 'align': 'center'})
            greenbg = workbook.add_format({'bg_color': '#33CC33'})
            redbg_bold = workbook.add_format({'bold': True, 'bg_color': '#FF3D01', 'align': 'center'})
            redbg = workbook.add_format({'bg_color': '#FF3D01'})
            money = workbook.add_format({'num_format': '$#,##0'})
            moneyYellow = workbook.add_format({'num_format': '$#,##0', 'bg_color': 'yellow'})
            moneybg = workbook.add_format({'num_format': '$#,##0', 'bg_color': '#37A4D5'})
            percent_fmt = workbook.add_format({'num_format': '0.00%'})
            # Main table on Ratio spreadsheet
            worksheet_ratio.write('K3', 'Per trade')
            worksheet_ratio.write('L3', '500', moneybg)
            worksheet_ratio.write('K4', 'Ratio', bold)
            worksheet_ratio.write('L4', '=K8/K10')
            worksheet_ratio.write('N3', 'Factor', bold)
            worksheet_ratio.write('O3', '=L3*O8', moneyYellow)
            worksheet_ratio.write('I8', 'Long: ', greenbg_bold)
            worksheet_ratio.write('I10', 'Short: ', redbg_bold)
            worksheet_ratio.write('J6', 'Stock', ocrebg_bold)
            worksheet_ratio.write('J8', longTicker, greenbg)
            worksheet_ratio.write('J10', shortTicker, redbg)
            worksheet_ratio.write('K6', 'Beta', ocrebg_bold)
            worksheet_ratio.write('K8', Utilities.getBetaFromFile(longTicker))
            worksheet_ratio.write('K10', Utilities.getBetaFromFile(shortTicker))
            worksheet_ratio.write('L6', 'Commit', ocrebg_bold)
            worksheet_ratio.write('L8', '100', moneybg)
            worksheet_ratio.write('L10', '=L8*L4', money)
            worksheet_ratio.write('M6', 'Price', ocrebg_bold)
            worksheet_ratio.write('M8', '=C2', money)
            worksheet_ratio.write('M10', '=C19', money)
            worksheet_ratio.write('N6', 'Shares', ocrebg_bold)
            worksheet_ratio.write('N8', '=L8/M8')
            worksheet_ratio.write('N10', '=L10/M10')
            worksheet_ratio.write('O6', '%', ocrebg_bold)
            worksheet_ratio.write('O8', '=L8/L12', percent_fmt)
            worksheet_ratio.write('O10', '=L10/L12', percent_fmt)
            worksheet_ratio.write('K12', 'Total', bold)
            worksheet_ratio.write('L12', '=L8+L10', money)

            # Table for LONG
            worksheet_ratio.write('A1', 'Date', greenbg_bold)
            worksheet_ratio.write_column(1, 0, acLCompleted.Date, date_format_long)
            worksheet_ratio.write('B1', 'Open', greenbg_bold)
            worksheet_ratio.write_column(1, 1, acLCompleted.Open)
            worksheet_ratio.write('C1', 'High', greenbg_bold)
            worksheet_ratio.write_column(1, 2, acLCompleted.High)
            worksheet_ratio.write('D1', 'Low', greenbg_bold)
            worksheet_ratio.write_column(1, 3, acLCompleted.Low)
            worksheet_ratio.write('E1', 'H-L', greenbg_bold)
            worksheet_ratio.write_column(1, 4, acLCompleted.HL)
            worksheet_ratio.write('F1', 'ATRP', greenbg_bold)
            worksheet_ratio.write_column(1, 5, acLCompleted.ATRP, percent_fmt)
            worksheet_ratio.write('E12', 'ATRP AVG', bold)
            worksheet_ratio.write('F12', '=AVERAGE(F2:F11)', percent_fmt)
            worksheet_ratio.write('E13', 'SL', greenbg_bold)
            worksheet_ratio.write('F13', '=C2-(C2*F12)', money)

            # Table for SHORT
            worksheet_ratio.write('A18', 'Date', redbg_bold)
            worksheet_ratio.write_column(18, 0, acSCompleted.Date, date_format_short)
            worksheet_ratio.write('B18', 'Open', redbg_bold)
            worksheet_ratio.write_column(18, 1, acSCompleted.Open)
            worksheet_ratio.write('C18', 'High', redbg_bold)
            worksheet_ratio.write_column(18, 2, acSCompleted.High)
            worksheet_ratio.write('D18', 'Low', redbg_bold)
            worksheet_ratio.write_column(18, 3, acSCompleted.Low)
            worksheet_ratio.write('E18', 'H-L', redbg_bold)
            worksheet_ratio.write_column(18, 4, acSCompleted.HL)
            worksheet_ratio.write('F18', 'ATRP', redbg_bold)
            worksheet_ratio.write_column(18, 5, acSCompleted.ATRP, percent_fmt)
            worksheet_ratio.write('E29', 'ATRP AVG', bold)
            worksheet_ratio.write('F29', '=AVERAGE(F19:F28)', percent_fmt)
            worksheet_ratio.write('E30', 'SL', redbg_bold)
            worksheet_ratio.write('F30', '=C19+(C19*F29)', money)

            worksheet_spread.write('A1', 'Date', bold)
            worksheet_spread.write_column(1, 0, adcLL.Date, date_format)
            worksheet_spread.write('B1', 'Long', greenbg_bold)
            worksheet_spread.write_column(1, 1, adcLL["Adj Close"])
            worksheet_spread.write('C1', 'Short', redbg_bold)
            worksheet_spread.write_column(1, 2, adcSL["Adj Close"])
            worksheet_spread.write('D1', 'Spread', ocrebg_bold)
            worksheet_spread.write_column(1, 3, spreads["{}-{}".format(longTicker, shortTicker)])
            worksheet_spread.write('F1', 'Ratio', bold)
            worksheet_spread.write('F2', ratio)

            chart = workbook.add_chart({'type': 'line'})
            chart.set_size({'x_scale': 1.5, 'y_scale': 2})
            chart.set_title({'name': 'Spread per Month'})
            chart.add_series({'categories': '=Spread!$A$2:$A$62'})
            chart.add_series({'values': '=Spread!$D$2:$D$62', 'name': 'Spread',
                              'trendline': {'type': 'linear', 'display_equation': False, 'name': 'Trend Line', 'line': {
                                  'color': 'red',
                                  'width': 2,
                              }},
                              })
            worksheet_spread.insert_chart('G5', chart)
            workbook.close()
        else:
            if len(acL) == len(acS):
                logging.error(
                    "The data length for {}-{} in downloadedData10mo is different. Please check manually.".format(
                        longTicker,
                        shortTicker))
            if len(adcLL) == len(adcSL):
                logging.error("The data length for {}-{} in Sectors\{} is different. Please check manually.".format(
                    longTicker,
                    shortTicker,
                    sector))
