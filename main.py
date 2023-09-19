#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys
import logging
import argparse
import traceback
import logging.handlers

from control import controller
from pprint import pformat


CONTROLLED_LEVELV_NUM = 29

logging.addLevelName(CONTROLLED_LEVELV_NUM, "CONTROLLED")


def controlled(self, message, *args, **kws):
    if self.isEnabledFor(CONTROLLED_LEVELV_NUM):
        # Yes, logger takes its '*args' as 'args'.
        self._log(CONTROLLED_LEVELV_NUM, message, args, **kws)

def start_logging(loggerPath, loggerName, loggerLevel):
    """
        Funcion para generar el archivo de logueo en la ruta pasada.
        Entrada:
            loggerPath: la ruta en donde se va a crear el archivo.
            loggerName: nombre del archivo de log, sin la extencion.
            loggerLevel: el nivel de logueo(debug, info, error)
        Salida:
            El objeto de logger que apunta al archivo.
    """
    # Setup local logger
    if not logging.getLogger(loggerName).handlers:
        # set logging level
        # level=logging.DEBUG
        level = int(logging.getLevelName(loggerLevel.upper()))
        # Create log file path
        logfile="%s/%s.log"%(loggerPath,loggerName)
        if not os.path.exists(logfile):
            with open(logfile, 'w') as f:
                pass
        # Create log file handler
        handler = logging.handlers.WatchedFileHandler(logfile)
        # Do not propagate to father
        logging.getLogger(loggerName).propagate=False
        # Set logging level
        logging.getLogger(loggerName).setLevel(level)
        # Set logging format
        handler.setFormatter(logging.Formatter("%(asctime)s.%(msecs)03d [%(process)d] [%(levelname)s] %(message)s",datefmt="%Y-%m-%d %H:%M:%S"))
        #
        logging.Logger.controlled = controlled
        # logging.getLogger(loggerName).controlled = controlled
        # Set logger handler
        logging.getLogger(loggerName).addHandler(handler)
    return logging.getLogger(loggerName)

# -------------------------------------------------------------------------------
#
# -------------------------------------------------------------------------------


class TradeEngine():
    '''
    Main class for a trade analysis engine. Reads a CSV and makes reports.
    '''

    def __init__(self, log=None):
        try:
            if not log:
                pass
            
            else:
                self.log = log

            self.controller = controller.Controller(self.log)

        except:
            error_info = ''.join(traceback.format_exception(*sys.exc_info()))
            self.log.error(error_info)
    
    def start_(self, option, csv_path='./data_example.csv', ticker=None, date=None):
        try:
            customer_data = self.controller.load_csv(csv_path)

            if customer_data:
                if option == 1:
                # self.log.info('Data load result: {}'.format(pformat(result[0])))
                    b_s_results = self.controller.buy_sell_by_ticker(customer_data)
                    self.log.info('Buy and sell calc: \n{}'.format(pformat(b_s_results)))
                    print(b_s_results)

                elif option == 2:
                    customer_trades = self.controller.customer_trades(customer_data)
                    self.log.info('Customer trades by date: \n{}'.format(pformat(customer_trades)))
                    print(customer_trades)

                elif option == 3:
                    ticker_average = self.controller.ticker_average(customer_data)
                    self.log.info('Tickers average: \n{}'.format(pformat(ticker_average)))
                    print(ticker_average)

                elif option == 4:
                    ticker_trades_by_date = self.controller.get_trades_by_ticker_date(customer_data)
                    # self.log.info('Tickers trades: {}'.format(pformat(ticker_trades_by_date)))

                    if ticker in ticker_trades_by_date:
                        if date in ticker_trades_by_date[ticker]:
                            print(ticker_trades_by_date[ticker][date])
                        
                        else:
                            self.log.error('Date not found on ticker trades.')
                    
                    else:
                        self.log.error('Ticker not found on data')
                
                else:
                    self.log.error("Option {} not supported.".format(option))
            
            else:
                self.log.error('No customers data found on path {}.'.format(csv_path))

        except:
            error_info = ''.join(traceback.format_exception(*sys.exc_info()))
            self.log.error(error_info)


if __name__ == '__main__':
    log = start_logging('./', 'trade_engine', 'info')

    parser = argparse.ArgumentParser("Trade Analysis report")
    parser.add_argument("csv_path", help="CSV file path")
    parser.add_argument("option", help="(1). Calculate the total buying and selling volume for each ticker. \n(2). Identify any customers that have more than 3 trades ina single day. \n(3). Average price for each ticker on days it was traded. \n(4). List of trades for a specific ticker and trade.")
    parser.add_argument("-t","--ticker", required=False, help="For option 4 required, ticker name to get the trades.")
    parser.add_argument("-d", "--date", required=False, help="For option 4 required, trade date with format YYYY-MM-DD to look for tickers.")

    args = parser.parse_args()

    log.info('Option: {}'.format(args.ticker))

    app = TradeEngine(log=log)
    if int(args.option):
        option= int(args.option)
        csv_path = args.csv_path

        ticker = args.ticker
        date = args.date

        app.start_(option, csv_path, ticker, date)
