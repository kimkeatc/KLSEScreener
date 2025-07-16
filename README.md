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
C:\Users\kimke\Desktop\workspace\KLSEScreener>python -m pip uninstall -y klsescreener
```

# Applications

## Development
```
C:\Users\KLSEScreener> python
>>>
>>> from klsescreener import klsescreener
>>> klsescreener.KLSEScreener().screener()
>>>
>>> from klsescreener import stock
>>> stock.Stock(stockcode="1818").info()
>>>
>>> exit()
C:\Users\KLSEScreener>
```
