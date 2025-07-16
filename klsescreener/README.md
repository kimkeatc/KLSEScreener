# klsescreener

## pytest

```
C:\Users\KLSEScreener> python -m pytest .\klsescreener\tests\
========================================================================================================== test session starts ==========================================================================================================
platform win32 -- Python 3.10.11, pytest-8.3.1, pluggy-1.5.0
rootdir: C:\Users\kimkchin\Desktop\KLSEScreener
plugins: anyio-4.8.0, time-machine-2.14.1
collected 29 items
klsescreener\tests\test_klsescreener.py .......                                                                                                                                                                                    [ 24%]
klsescreener\tests\test_stock.py ......................                                                                                                                                                                            [100%]
=========================================================================================================== warnings summary ============================================================================================================ 
klsescreener/tests/test_klsescreener.py: 7 warnings
klsescreener/tests/test_stock.py: 8 warnings
  C:\Users\kimkchin\Desktop\KLSEScreener\klsescreener\klsescreener.py:34: FutureWarning: Passing literal html to 'read_html' is deprecated and will be removed in a future version. To read from a literal string, wrap it in a 'StringIO' object.
    dataframes = pandas.read_html(io=response.text, match=match, extract_links=extract_links)
-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
=================================================================================================== 29 passed, 15 warnings in 39.18s ====================================================================================================
PS C:\Users\kimkchin\Desktop\KLSEScreener> 
```
