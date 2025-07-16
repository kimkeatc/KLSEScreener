# KLSEScreener
https://www.klsescreener.com/v2/ related function.

# Uninstall package
```
C:\Users\KLSEScreener> python -m pip uninstall -y KLSEScreener
```

# Install package
```
C:\Users\KLSEScreener> python -m pip install -e .
```

# Build *.whl file
```
C:\Users\KLSEScreener> python -m pip install build
C:\Users\KLSEScreener> python -m build
```

# Install package via *.whl file
```
C:\Users\KLSEScreener> python -m pip install --find-links=.\dist KLSEScreener
```

# Clean up
```
C:\Users\KLSEScreener> RMDIR /S /Q dist build libs\KLSEScreener.egg-info 2>NUL
```

# Verify package
```
C:\Users\KLSEScreener> python -c "import klsescreener; print(dir(klsescreener))"
```

# Run test
```
C:\Users\KLSEScreener> pytest
================================================================= test session starts ==================================================================
platform win32 -- Python 3.14.0, pytest-9.0.2, pluggy-1.6.0
rootdir: D:\kimkeatc\KLSEScreener
configfile: pytest.ini
collected 34 items                                                                                                                                      

libs\klsescreener\tests\test_screener.py ...........                                                                                              [ 32%]
libs\stock\tests\test_stock.py .......................                                                                                            [100%]

============================================================ 34 passed in 272.44s (0:04:32) ============================================================
```
