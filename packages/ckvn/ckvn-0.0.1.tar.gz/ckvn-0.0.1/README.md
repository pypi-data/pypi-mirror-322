Để đảm bảo bạn có thể dễ dàng copy toàn bộ nội dung Markdown vào file của bạn, tôi sẽ loại bỏ các khối mã thụt đầu dòng và cung cấp nội dung dạng text gọn gàng hơn:

---

# CKVN

CKVN is a Python module that allows you to interact with stock market data through a Django-based API. It provides various functions to retrieve stock information, historical data, and more by making API calls.

## Features

- **Get stock information**: Retrieve detailed information about a stock, including its name, symbol, and other metadata.  
- **Get historical stock data**: Retrieve the stock data (OHLCV) for a given stock over a specified date range.  
- **Get stocks by market**: Fetch stocks associated with a specific market (e.g., HOSE, HNX).  
- **Get API key info**: Retrieve information about the API key, including expiration date and status.  
- **API key authentication**: Use API keys to authenticate requests for accessing stock data.  

## Installation

You can install the `ckvn` module directly from PyPI using pip:

```bash
pip install ckvn
```

## Usage

### Getting Stock Information

You can retrieve information about a stock by symbol using the `get_stock_info()` function:

```python
import ckvn

symbol = 'AAPL'  # Example stock symbol
api_key = 'your_api_key'

stock_info = ckvn.get_stock_info(symbol, api_key)
print(stock_info)
```

### Getting Historical Stock Data

To retrieve historical stock data (OHLCV) for a given stock symbol within a date range:

```python
import ckvn
from datetime import datetime

symbol = 'AAPL'
api_key = 'your_api_key'
from_date = datetime(2020, 1, 1)
to_date = datetime(2021, 1, 1)

stock_data = ckvn.get_stock_data(symbol, from_date, to_date, api_key)
print(stock_data)
```

### Getting Stocks by Market

You can fetch all stocks associated with a particular market:

```python
import ckvn

market = 'HOSE'  # Example market
api_key = 'your_api_key'

stocks = ckvn.get_stocks_by_market(market, api_key)
print(stocks)
```

### Getting API Key Info

To retrieve information about your API key, such as expiration date, status, and other details, you can use the `get_key_info()` function:

```python
import ckvn

api_key = 'your_api_key'

key_info = ckvn.get_key_info(api_key)
print(key_info)
```

## Authentication

Each request made to the API requires an API key for authentication. Make sure to pass a valid API key when calling any of the functions above.

## Contributing

We welcome contributions to this project! If you'd like to help, please fork the repository, make your changes, and submit a pull request. Be sure to follow the code of conduct and review the guidelines before contributing.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

If you have any questions or suggestions, feel free to reach out to us at [ckvnpro@gmail.com](mailto:ckvnpro@gmail.com).