# KLSEScreener
https://www.klsescreener.com/v2/ related function.

# Build *.whl file
```
C:\Users\KLSEScreener> RMDIR /s /q build dist klsescreener.egg-info
C:\Users\KLSEScreener> python setup.py sdist bdist_wheel
```

# Install package *.whl files under sub-directory, dist
```
C:\Users\KLSEScreener> python -m pip install --find-links=.\dist klsescreener
```

# Uninstall package
```
C:\Users\KLSEScreener> python -m pip uninstall -y klsescreener
```

# Applications

## Development
```
C:\Users\KLSEScreener> python
>>>
>>> from klsescreener.klsescreener import KLSEScreener
>>> from klsescreener.stock import Stock
>>>
>>> # Bursa Index
>>> KLSEScreener().bursa_index_components()
>>>
>>> # Stocks screener
>>> KLSEScreener().screener()
>>>
>>> # Warrants screener
>>> KLSEScreener().warrant_screener()
>>>
>>> stock = Stock(stockcode="1818")
>>> stock.info()
>>>
>>> stock..get_listing_date(return_timestamp=True)
>>>
>>> stock.historical_data_1D()
>>>
>>> exit()
C:\Users\KLSEScreener>
```
