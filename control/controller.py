import os 
import sys
import csv
import traceback

from pprint import pformat


class Controller():
    
    def __init__(self, log):
        self.log = log

    def load_csv(self, path):
        '''
        Loads a csv and returns a dict object.
        '''
        try:
            result = None
            with open(path, 'r') as csvfile:
                dictobj = csv.DictReader(csvfile, skipinitialspace=True, delimiter=',', )
            
                if dictobj:
                    result = list(dictobj)
        except:
            error_info = ''.join(traceback.format_exception(*sys.exc_info()))
            self.log.error(error_info)

        return result

    def get_data(self, found_, customer_data):
        '''
        Returns a list of elements founded on a dict giving a key. 
        '''
        try:
            result = []
            for data in customer_data: 
                if data[found_] not in result:
                    result.append(data[found_])

            # self.log.info('Result found: {}'.format(pformat(result)))

        except:
            error_info = ''.join(traceback.format_exception(*sys.exc_info()))
            self.log.error(error_info)
        
        return result

    def buy_sell_by_ticker(self, customers_data):
        try:
            final_data = {}
            tickers = self.get_data('ticker', customers_data)
            for ticker in  tickers:
                final_data[ticker] = {
                    'BUY':0, 
                    'SELL':0
                }

            for customer_data in customers_data:
                try:
                    final_data[customer_data['ticker']][customer_data['trade_type']] += float(customer_data['quantity'])
                    final_data[customer_data['ticker']][customer_data['trade_type']] += float(customer_data['quantity'])
                
                except:
                    self.log.info('Unknow trade type, log report:')
                    error_info = ''.join(traceback.format_exception(*sys.exc_info()))
                    self.log.error(error_info)
                    continue

        except:
            error_info = ''.join(traceback.format_exception(*sys.exc_info()))
            self.log.error(error_info)
        
        return final_data

    def customer_trades(self, customers_data):
        try:
            final_data = {}
            customers = self.get_data('customer_id', customers_data)
            dates = self.get_data('trade_date', customers_data)

            for customer in customers:
                final_data[customer] = {}
                for date in dates:
                    final_data[customer][date] = {
                        'trades': 0
                        }
                    
            for data in customers_data:
                # self.log.info('Processing data: {}'.format(data))
                final_data[data['customer_id']][data['trade_date']]['trades'] += 1

        except:
            error_info = ''.join(traceback.format_exception(*sys.exc_info()))
            self.log.error(error_info)
        
        return final_data
            
    def ticker_average(self, customers_data):
        try:
            dates = self.get_data('trade_date', customers_data)
            tickers = self.get_data('ticker', customers_data)

            final_data = {}
            for ticker in tickers:
                final_data[ticker] = {}
                for date in dates:
                    final_data[ticker][date] = {
                        'average': 0.0,
                        'total' : 0.0,
                        'trades': 0
                    }
            
            for customer_data in customers_data:
                final_data[customer_data['ticker']][customer_data['trade_date']]['total'] += float(customer_data['price'])
                final_data[customer_data['ticker']][customer_data['trade_date']]['trades'] += 1
            
            for ticker_data in final_data:
                for date in dates:
                    final_data[ticker_data][date]['average'] = final_data[ticker_data][date]['total']/final_data[ticker_data][date]['trades'] if final_data[ticker_data][date]['trades'] else 0

        except:
            error_info = ''.join(traceback.format_exception(*sys.exc_info()))
            self.log.error(error_info)
        
        return final_data

    def get_trades_by_ticker_date(self, customers_data, ticker='', date=''):
        try:
            final_data = {}
            
            if not ticker and not date:
                dates = self.get_data('trade_date', customers_data)
                tickers = self.get_data('ticker', customers_data)

                for ticker in tickers:
                    final_data[ticker] = {}
                    for date in dates:
                        final_data[ticker][date] = []
            
                for customer_data in customers_data:
                    final_data[customer_data['ticker']][customer_data['trade_date']].append(customer_data)
            
            else:
                final_data[ticker] = []
                for customer_data in customers_data:
                    if customer_data['ticker'] == ticker and customer_data['trade_date'] == date:
                        final_data[ticker].append(customer_data)

        except:
            error_info = ''.join(traceback.format_exception(*sys.exc_info()))
            self.log.error(error_info)
        
        return final_data

