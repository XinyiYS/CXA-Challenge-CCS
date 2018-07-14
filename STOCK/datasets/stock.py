import config
import pandas as pd
import os
import intrinio
intrinio.client.username = config.intrinio_config['intrinio_user']
intrinio.client.password = config.intrinio_config['intrinio_pw']
# print(intrinio.prices('AAPL', start_date='2016-01-01'))
# print(intrinio.financials('AAPL'))

def create_datasets(company):

	# 'AAPL','GOOG'
	df_1 = (intrinio.prices(company))
	df_2 = (intrinio.financials(company))
	df_1.to_csv(company+'_prices.csv')
	df_2.to_csv(company+'_financials.csv')

	return

companies = ['AAPL','GOOG','AMZN','FB','MSFT','MSI']


[create_datasets(company) for company in companies]





# print(intrinio.companies(query='Bank'))
