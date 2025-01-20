import requests

API_BASE_URL = 'https://amistock.com/stockdata/'

def get_stock_info(symbol, api_key):
    headers = {'Authorization': api_key}
    response = requests.get(f'{API_BASE_URL}get_stock_info/{symbol}/', headers=headers)
    return response.json()

def get_stock_data(symbol, from_date, to_date, api_key):
    headers = {'Authorization': api_key}
    response = requests.get(f'{API_BASE_URL}get_stock_data/{symbol}/{from_date}/{to_date}/', headers=headers)
    return response.json()

def get_stocks_by_market(market, api_key):
    headers = {'Authorization': api_key}
    response = requests.get(f'{API_BASE_URL}get_stocks_by_market/{market}/', headers=headers)
    return response.json()

def get_key_info(api_key):
    headers = {'Authorization': api_key}
    response = requests.get(f'{API_BASE_URL}get-key-info/', headers=headers)
    return response.json()