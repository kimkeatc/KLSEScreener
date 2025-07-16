#!/usr/bin/env python

# -*- coding: utf-8 -*-

# Import standard libraries
import threading
import logging
import ast
import sys

# Import custom script
try:
    from stock import Stock
    from klsescreener import KLSEScreener
    from misc import dec_performance, chunks
except ImportError:
    from .stock import Stock
    from .klsescreener import KLSEScreener
    from .misc import dec_performance, chunks

NUMBER_OF_THREADS = 16


if __name__ == "__main__":

    # Setup logging
    logger = logging.getLogger(name=None)
    if logger.hasHandlers():
        logger.handlers.clear()
    logger.setLevel(level=logging.INFO)

    # Create a stream handler
    stream_handler = logging.StreamHandler(stream=sys.stdout)
    stream_handler.setFormatter(
        fmt=logging.Formatter(
            fmt="[%(thread)5s] [%(threadName)32s] [%(asctime)s] [%(levelname)8s] : %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
    )
    logger.addHandler(hdlr=stream_handler)

    # Collect data - Bursa index
    results = {}
    for _, row in KLSEScreener().bursa_index_components().iterrows():
        results.setdefault(row["Code"], {
            "Code": row["Code"],
            "Name": row["Index"],
            "Link": row["Link"],
            "Chart Link": row["Chart Link"],
            "Components": [] if isinstance(row["Components"], float) else ast.literal_eval(row["Components"]),
        })

    # Collect data - Stocks
    @dec_performance(log=logging.info)
    def mThread_update_stock(stockcodes: list[str], number_of_threads: int = NUMBER_OF_THREADS):
        length_stockcodes = len(stockcodes)
        logging.info(f"Number of stockcodes that require processing: {length_stockcodes}")
        if length_stockcodes <= number_of_threads:
            number_of_threads = length_stockcodes
        logging.info(f"Number of threads will be allocated: {number_of_threads}")

        threads, results = [], {}
        stockcodes = chunks(iterable=stockcodes, n=number_of_threads)
        for stockcode in stockcodes:
            threads.append(threading.Thread(
                target=sThread_update_stock,
                args=[stockcode, results]
            ))
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

        logging.info("All threads have completed.")
        return results

    def sThread_update_stock(stockcodes: list[str], results: dict = {}):
        length_stockcodes = len(stockcodes)
        dataframe = KLSEScreener().screener()
        for index, stockcode in enumerate(stockcodes, start=1):
            logging.info(f"Processing stock code {index:03d}/{length_stockcodes:03d} - {stockcode}")
            row = dataframe[dataframe["Code"] == stockcode].iloc[0]
            result = results.setdefault(stockcode, {
                "Code": stockcode,
                "Name": "",
                "Category": "",
                "Listing Date": "",
                "Link": row["KLSEScreener"],
                "Chart Link": row["KLSEScreener Chart"],
                "History": {},
            })
            if result["Name"] != row["Name"]:
                logging.debug(f"Update stock code {stockcode} name from {result['Name']} to {row['Name']}.")
                result["Name"] = row["Name"]
            if result["Category"] != row["Category"]:
                logging.debug(f"Update stock code {stockcode} category from {result['Category']} to {row['Category']}.")
                result["Category"] = row["Category"]
            if result["Listing Date"] == "":
                result["Listing Date"] = Stock(stockcode=stockcode).get_listing_date(fmt="%Y-%m-%d")
        return results

    results = mThread_update_stock(stockcodes=KLSEScreener().screener()["Code"].to_list())
    logging.info(results)
