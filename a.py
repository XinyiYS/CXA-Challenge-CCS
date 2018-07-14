from iexfinance import Stock
tsla = Stock('TSLA')
print(tsla.get_open())
print(tsla.get_price())

from iexfinance import get_historical_data
from datetime import datetime

start = datetime(2017, 2, 9)
end = datetime(2017, 5, 24)

# df = get_historical_data("AAPL", start=start, end=end, output_format='pandas')


from iexfinance import get_stats_intraday

print(get_stats_intraday())