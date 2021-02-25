# Stock Analysis and Prediction System
Stock analysis and prediction system works on the stratergy of Moving Average (MA), Fibonacci Retracement and Heikin Ashi,
to predict the forthcoming stock price of the companies listed in NSE.

## Introduction
Stock market prediction aims to determine the future movement of the stock value of a financial exchange.
The accurate prediction of share price movement will lead to more profit investors can make. Predicting how the
stock market will move is one of the most challenging issues due to many factors that involved in the stock prediction,
such as interest rates, politics, and economic growth that make the stock market volatile and very hard to predict accurately.

## Description
This application is made using Python Programming Language's DJANGO Framework. A user can register to the portal by providing a username and 
his e-mail id. The e-mail id is then validated by sending  a confirmation mail, from which he/she can activate their account.

After activation of their account a user can log-in to the dashboard where the predicted stock price (Stock trade calls) which consists of
4 Targets and a Stop Loss will be displayed. These stock trade calls are displayed by analysing the past data's Moving Average .Instead
of using simple candle sticks for calculating moving average we have made use of Heikin Ashi Candles ("average bar" in Japanese) for reducing the noise
of the irregular data, and finally for calculating the target values Fibonacci Retracement has been used.

These stock trade calls are updated every day at 07:00 Hrs IST automatically using 'AP scheduler'.

Latest market news is updated every 1Hr using NEWS API. We have made a reports page where the reports of all the companies whose stock trade calls 
had been given by us in the recent past can be downloaded.

The accuracy of this model is around 80%. 

This project is hosted on heroku server under the domain name of www.investinit.ml (http://www.investinit.ml) and can be accessed by visiting the same.

## Features
- Daily Stock analytical tips
- Latest News related to market
- Downloadable reports

## Technology Stack

- Python 3.8
- Django3
- HTML, CSS, JS and Bootstrap
- AP Scheduler
- NumPy and Pandas Library
