#!/usr/bin/env python

# -*- coding: utf-8 -*-

# Import standard libraries
from os.path import dirname, exists, join
from datetime import datetime
from enum import Enum, auto
import threading
import logging
import json
import sys
import os

# Import third-party libraries
import pandas

# Import custom script
try:
    from stock import Stock
    from misc import dec_performance
    from klsescreener import KLSEScreener
except ImportError:
    from .stock import Stock
    from .misc import dec_performance
    from .klsescreener import KLSEScreener

__TIMESTAMP__ = datetime.now().strftime(format="%Y-%m-%d %H:%M:%S")


class ConfigKey(Enum):
    index = auto()
    screener = auto()
    warrant = auto()


class Analysis:

    def __init__(self, workspace: str):
        self.workspace = workspace
        # Define the configuration file path
        self.configname = "config.json"
        self.configpath = join(self.workspace, self.configname)
        self.config = self.load_config()

    def _setup_workspace(self):
        """Initialize the workspace.
        """
        os.makedirs(name=self.workspace, mode=0o775, exist_ok=True)

    def load_config(self):
        """Load configuration from the config file.
        """
        # Create config file if it does not exist
        if not exists(self.configpath):
            data = {
                ConfigKey.index.name: {},
                ConfigKey.screener.name: {},
                ConfigKey.warrant.name: {}
            }
            with open(file=self.configpath, mode="w", encoding="utf-8") as fh:
                json.dump(obj=data, fp=fh, indent=4)
        # Load config from file
        with open(file=self.configpath, mode="r", encoding="utf-8") as fh:
            config = json.load(fp=fh)
        return config
    @dec_performance

    def update_config(self, update_screener: bool = True, update_warrant: bool = True, update_index: bool = True):
        """Update the configuration file with new information.
        """
        klsescreener = KLSEScreener()
        if update_screener is True:
            logging.info(f"Updating {self.configpath} - Stock.")
            dataframe = klsescreener.screener()
            config = self.config.setdefault(ConfigKey.screener.name, {})
            threads = []
            number_of_threads = 16
            def sThread_update_config_screener(dataframe: pandas.Series, result: dict):
                for _, row in dataframe.iterrows():
                    code, name = row["Code"], row["Name"]
                    stock_result = result.setdefault(code, {})
                    if stock_result == {}:
                        logging.info(f"Updating stock code {code:6s} - {name}")
                        listing_date = Stock(stockcode=code).get_listing_date()
                        stock_result["Code"] = code
                        stock_result["Name"] = ""
                        stock_result["Category"] = ""
                        stock_result["Listing Date"] = listing_date.strftime("%Y-%m-%d") if listing_date else ""
                        stock_result["KLSEScreener"] = row["KLSEScreener"]
                        stock_result["KLSEScreener Chart"] = row["KLSEScreener Chart"]
                    stock_result["Name"] = name
                    stock_result["Category"] = row["Category"]
                    stock_result["Last Updated"] = __TIMESTAMP__
            number_of_rows_to_handle_per_thread = len(dataframe) // number_of_threads
            for i in range(number_of_threads):
                threads.append(threading.Thread(
                    target=sThread_update_config_screener,
                    args=[
                        dataframe.iloc[i * number_of_rows_to_handle_per_thread: (i + 1) * number_of_rows_to_handle_per_thread],
                        config
                    ]
                ))
            for thread in threads:
                thread.start()
            for thread in threads:
                thread.join()
            self.config[ConfigKey.screener.name] = dict(sorted(config.items()))
        if update_warrant is True:
            logging.warning("Update warrant is not implemented yet.")
        if update_index is True:
            logging.info(f"Updating {self.configpath} - Bursa Index.")
            dataframe = klsescreener.bursa_index_components()
            config = self.config.setdefault(ConfigKey.index.name, {})
            for _, row in dataframe.iterrows():
                components = row["Components"]
                components = [] if isinstance(components, float) else components.split(";")
                components.sort(reverse=False)
                config[row["Code"]] = {
                    "Code": row["Code"],
                    "Name": row["Index"],
                    "Components": components,
                    "Link": row["Link"],
                    "Chart Link": row["Chart Link"],
                    "Last Updated": __TIMESTAMP__,
                }
        with open(file=self.configpath, mode="w", encoding="utf-8") as fh:
            json.dump(obj=self.config, fp=fh, indent=4)


def setup_logging():
    logger = logging.getLogger(name=None)
    if logger.hasHandlers():
        logger.handlers.clear()
    logger.setLevel(level=logging.INFO)
    # Create a stream handler
    stream_handler = logging.StreamHandler(stream=sys.stdout)
    stream_handler.setFormatter(
        fmt=logging.Formatter(
            fmt="[%(thread)5s] [%(threadName)45s] [%(asctime)s] [%(levelname)8s] : %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
    )
    logger.addHandler(hdlr=stream_handler)


if __name__ == "__main__":
    setup_logging()
    analysis = Analysis(workspace=dirname(__file__))
    analysis._setup_workspace()
    analysis.update_config()
