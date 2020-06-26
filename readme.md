# Investing_portfolio

This program allows you to invest in the stock market based on the web TipRanks advisors.
Based on the idea to buy and sell two different stocks at the same time from the same sector, and from there analyse different set of data to calculate where to put the StopLoss and depending how much you want to trade, it will tell you how you should split the money in the pair of stocks.

Notes: The program generate two log files:
* app.log: Store all the events from the processing data side, and main error when is downloading data from internet.
* appDownloads.log: Store all the event from internet side, errors and minors events also.
## Requrements
    pip install pandas
    pip install numpy
    pip install beautifulsoup4
    pip install requests
    pip install lxml
    pip install XlsxWriter
    
## Instructions
The first thing to do is upload the files one by one from the folder toTipRanks with the following procedure:

1. Go to the website, using the private web browser: https://www.tipranks.com/smart-portfolio/
2. You need to upload each file from toTipRanks 

![home](https://github.com/rgutmen/portfolioTR/blob/master/resources/1.png)

3. Once the website has loaded all the tickers, press the 'detailed' button.

![detailed](https://github.com/rgutmen/portfolioTR/blob/master/resources/2.png)

4. On the bottom of the website press the option 'Add Metrics to Chart'
![metricsToChart](https://github.com/rgutmen/portfolioTR/blob/master/resources/3.png)

5. Mark the checkbox as they are in the image.
![makrs](https://github.com/rgutmen/portfolioTR/blob/master/resources/4.png)

6. Once it has finish, is time to download the file on the folder: FromTipRanks
7. Repeat the process for each file (This is the tedious part :S ).
8. Execute the program and wait! It will take 5-10 min.


    > python main.py FromTipRanks 20 True
    o
    > python main.py FromTipRanks 20 False
    
Parameters:
   * Folder where are located the csv from TipRanks (Previous steps 1-7)
   * A number, this number is the number of trades to analyse.
        * For example: 20.
   * A boolean parameter:
        * True: None from all the stocks is repeatable. 
            - For example: In the case the pair AMZN-AAPL, AMZN and AAPL is not any more in the set (20) of all pairs.
        * False: The stocks are repeatable. 
            - For example: In the case the pair AMZN-AAPL, exist the chance that one of this stocks can be combined with other, so is easy to get something like AMZN-GMC, AMZN-GOOG in the set (20) of all pairs.

## Functionality
The program is splited in 7 main functions each of them save the data into files, and the next function read this parameters from the disk. This make everything easy to follows in case to update the program or just get the data files in some point.
1. Create the folder structure and from the downloaded file from TipRanks, read and organize all of them by sector and also in Buy/Sell according TipRanks advisors.
2. Download all the data for each ticker from yahoo services. This is the longer part. You need to be patient.
3. Put all the 'Adj. Close' from the previous step in one .csv file, for Buy and Sell for each sector.
4. From the previous files, for each sector, it does all the possible combinations calculating the Buy['Adj. Close'] / Sell['Adj. Close], in order to get the spread. And for each combination Buy/Sell ['Adj. Close] for the last 5 years, it reduce all this data to a single number, called ratio. This ratio is the 'polyfit' function and it's saved also in a file.
5. From all the ratios previous calculated and sorted in the descending order, just are selected the amount of pairs assigned as parameter, also considering the boolean parameter (if the tickers are repeatable or not).
6. **At this point, the program has calculated which are the stocks to invest.**
7. Download the data for the last months and the Beta from yahoo, for the stocks to invest.
8. With all this data it generate a excel file (with two tabs) for each pair. 
    * Ratio tab: 
        * In the blue cell, next where it says: 'Per trade'. The user has to insert the amount of money to invest in this pair.
        * In the blue cell, below where it says: 'Commit'. The user has to insert the amount in the yellow cell.
        * In the green cell, next where it says: 'SL'. Is the StopLoss for the LONG ticker.
        * In the red cell, next where it says: 'SL'. Is the StopLoss for the SHORT ticker.
    * Spread tab (it gives information about why this pair was selected): 
        * Is possible to visualize the 'Adj. Close' for Long and Short, also the spread (Long/Short) and the graph with the ratio.
   
## What I have learn?
I have learn about:
* Pandas.
* Numpy.
* Web scraping.
* Trading.

## Improvements
* Research on web scraping in order to upload the files to TipRanks and get them all automatically.
* Research on trading in order to make a different strategy. 
