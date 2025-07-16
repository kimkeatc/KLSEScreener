#!/usr/bin/env python

# -*- coding: utf-8 -*-

# Import standard libraries
from os.path import dirname, exists, join
import datetime
import logging
import json

# Import third-party libraries
import pandas

# Import custom script
try:
    from klsescreener.klsescreener import KLSEScreener
    from klsescreener.resolution import Resolution
    from klsescreener.misc import dec_performance
except ImportError:
    from .klsescreener import KLSEScreener
    from .resolution import Resolution
    from .misc import dec_performance


class Stock(KLSEScreener):

    def __init__(self, stockcode: str):
        super().__init__()
        self.stockcode = stockcode
        self.stockcode_url = f"{self.url}/stocks/view/{self.stockcode}"
        # Define the configuration file path
        self.config_filename = r"config.json"
        self.config_filepath = join(dirname(__file__), self.config_filename)
        self.config = self.load_config()

    @dec_performance
    def load_config(self):
        """Load configuration from JSON file."""
        # Create config file if it does not exist
        if not exists(self.config_filepath):
            with open(file=self.config_filepath, mode="w", encoding="utf-8") as fh:
                json.dump(obj={}, fp=fh)
        # Load config from file
        with open(file=self.config_filepath, mode="r", encoding="utf-8") as fh:
            config = json.load(fp=fh)
        return config

    @dec_performance
    def info(self):
        return self.fetch_html(url=self.stockcode_url)[0].dropna()

    @dec_performance
    def quarter_reports(self):
        dataframe = self.fetch_html(url=self.stockcode_url, match="Financial Year", extract_links="all")[0].iloc[:, :13]
        dataframe = self._post_process_dataframe(dataframe)
        return dataframe

    @dec_performance
    def annual_reports(self):
        dataframe = self.fetch_html(url=self.stockcode_url, match="Financial Year", extract_links="all")[1]
        dataframe = self._post_process_dataframe(dataframe)
        return dataframe

    @dec_performance
    def dividend_reports(self):
        dataframe = self.fetch_html(url=self.stockcode_url, match="Financial Year", extract_links="all")[2].iloc[:, :8]
        dataframe = self._post_process_dataframe(dataframe)
        return dataframe

    @dec_performance
    def capital_changes(self):
        dataframe = self.fetch_html(url=self.stockcode_url, match="Ratio", extract_links="all")[0]
        dataframe = self._post_process_dataframe(dataframe)
        return dataframe

    @dec_performance
    def warrants(self):
        dataframe = self.fetch_html(url=self.stockcode_url, extract_links="all")[-2]
        dataframe = self._post_process_dataframe(dataframe)
        return dataframe
    @dec_performance
    def shareholding_changes(self):
        return self.fetch_html(url=self.stockcode_url, match="Date Change")[0]

    def historical_data(self, resolution: str, stimestamp: int, etimestamp: int, countback: int = 99999999) -> pandas.DataFrame:
        url = f"{self.url}/trading_view/history?symbol={self.stockcode}&resolution={resolution}&from={stimestamp}&to={etimestamp}&countback={countback}&currencyCode=MYR"
        logging.debug(f"Fetching historical data for stockcode \"{self.stockcode}\" with resolution {resolution} from {datetime.datetime.fromtimestamp(stimestamp)} ({stimestamp}) to {datetime.datetime.fromtimestamp(etimestamp)} ({etimestamp}). {url}")
        dataframe = self.fetch_json(url=url)
        # Post-process the dataframe
        dataframe.insert(loc=0, column="d", value=pandas.to_datetime(dataframe["t"], unit="s") + pandas.to_timedelta("8 hours"))
        dataframe.insert(loc=0, column="Time", value=dataframe["d"].dt.time)
        dataframe.insert(loc=0, column="Date", value=dataframe["d"].dt.date)
        dataframe.insert(loc=0, column="Month", value=dataframe["d"].dt.month)
        dataframe.insert(loc=0, column="Year", value=dataframe["d"].dt.year)
        dataframe.insert(loc=0, column="Resolution", value=resolution)
        dataframe.drop(columns=["s", "from", "to", "exact_from", "server", "ip", "qt"], axis=1, inplace=True)
        dataframe.sort_values(by=["t"], ascending=False, inplace=True)
        dataframe.reset_index(drop=True, inplace=True)
        logging.debug(f"Fetched {len(dataframe)} rows of historical data for stockcode \"{self.stockcode}\" with resolution {resolution} from {datetime.datetime.fromtimestamp(stimestamp)} ({stimestamp}) to {datetime.datetime.fromtimestamp(etimestamp)} ({etimestamp}).")
        return dataframe

    @dec_performance
    def historical_data_1m(self, stimestamp: int = int((datetime.datetime.now() - datetime.timedelta(days=360)).timestamp()), etimestamp: int = int(datetime.datetime.now().timestamp())) -> pandas.DataFrame:
        return self.historical_data(resolution=Resolution.MINUTE_1.value, stimestamp=stimestamp, etimestamp=etimestamp)

    @dec_performance
    def historical_data_5m(self, stimestamp: int = int((datetime.datetime.now() - datetime.timedelta(days=360)).timestamp()), etimestamp: int = int(datetime.datetime.now().timestamp())) -> pandas.DataFrame:
        return self.historical_data(resolution=Resolution.MINUTE_5.value, stimestamp=stimestamp, etimestamp=etimestamp)

    @dec_performance
    def historical_data_15m(self, stimestamp: int = int((datetime.datetime.now() - datetime.timedelta(days=360)).timestamp()), etimestamp: int = int(datetime.datetime.now().timestamp())) -> pandas.DataFrame:
        return self.historical_data(resolution=Resolution.MINUTE_15.value, stimestamp=stimestamp, etimestamp=etimestamp)

    @dec_performance
    def historical_data_30m(self, stimestamp: int = int((datetime.datetime.now() - datetime.timedelta(days=360)).timestamp()), etimestamp: int = int(datetime.datetime.now().timestamp())) -> pandas.DataFrame:
        return self.historical_data(resolution=Resolution.MINUTE_30.value, stimestamp=stimestamp, etimestamp=etimestamp)

    @dec_performance
    def historical_data_1H(self, stimestamp: int = int((datetime.datetime.now() - datetime.timedelta(days=360)).timestamp()), etimestamp: int = int(datetime.datetime.now().timestamp())) -> pandas.DataFrame:
        return self.historical_data(resolution=Resolution.HOUR_1.value, stimestamp=stimestamp, etimestamp=etimestamp)

    @dec_performance
    def historical_data_4H(self, stimestamp: int = int((datetime.datetime.now() - datetime.timedelta(days=360)).timestamp()), etimestamp: int = int(datetime.datetime.now().timestamp())) -> pandas.DataFrame:
        return self.historical_data(resolution=Resolution.HOUR_4.value, stimestamp=stimestamp, etimestamp=etimestamp)

    @dec_performance
    def historical_data_1D(self, stimestamp: int = int((datetime.datetime.now() - datetime.timedelta(days=360)).timestamp()), etimestamp: int = int(datetime.datetime.now().timestamp())) -> pandas.DataFrame:
        return self.historical_data(resolution=Resolution.DAILY.value, stimestamp=stimestamp, etimestamp=etimestamp)

    @dec_performance
    def historical_data_1W(self, stimestamp: int = int((datetime.datetime.now() - datetime.timedelta(days=360)).timestamp()), etimestamp: int = int(datetime.datetime.now().timestamp())) -> pandas.DataFrame:
        return self.historical_data(resolution=Resolution.WEEKLY.value, stimestamp=stimestamp, etimestamp=etimestamp)

    @dec_performance
    def historical_data_1M(self, stimestamp: int = int((datetime.datetime.now() - datetime.timedelta(days=360)).timestamp()), etimestamp: int = int(datetime.datetime.now().timestamp())) -> pandas.DataFrame:
        return self.historical_data(resolution=Resolution.MONTH_1.value, stimestamp=stimestamp, etimestamp=etimestamp)

    @dec_performance
    def historical_data_3M(self, stimestamp: int = int((datetime.datetime.now() - datetime.timedelta(days=360)).timestamp()), etimestamp: int = int(datetime.datetime.now().timestamp())) -> pandas.DataFrame:
        return self.historical_data(resolution=Resolution.MONTH_3.value, stimestamp=stimestamp, etimestamp=etimestamp)

    @dec_performance
    def historical_data_6M(self, stimestamp: int = int((datetime.datetime.now() - datetime.timedelta(days=360)).timestamp()), etimestamp: int = int(datetime.datetime.now().timestamp())) -> pandas.DataFrame:
        return self.historical_data(resolution=Resolution.MONTH_6.value, stimestamp=stimestamp, etimestamp=etimestamp)

    @dec_performance
    def historical_data_1Y(self, stimestamp: int = int((datetime.datetime.now() - datetime.timedelta(days=360)).timestamp()), etimestamp: int = int(datetime.datetime.now().timestamp())) -> pandas.DataFrame:
        return self.historical_data(resolution=Resolution.YEAR_1.value, stimestamp=stimestamp, etimestamp=etimestamp)

    @dec_performance
    def historical_data_5Y(self, stimestamp: int = int((datetime.datetime.now() - datetime.timedelta(days=360)).timestamp()), etimestamp: int = int(datetime.datetime.now().timestamp())) -> pandas.DataFrame:
        return self.historical_data(resolution=Resolution.YEAR_5.value, stimestamp=stimestamp, etimestamp=etimestamp)

    @dec_performance
    def historical_data_10Y(self, stimestamp: int = int((datetime.datetime.now() - datetime.timedelta(days=360)).timestamp()), etimestamp: int = int(datetime.datetime.now().timestamp())) -> pandas.DataFrame:
        return self.historical_data(resolution=Resolution.YEAR_10.value, stimestamp=stimestamp, etimestamp=etimestamp)

    @dec_performance
    def get_listing_date(self) -> datetime.date:
        # First quarter report
        date = self.quarter_reports()["Q Date"].to_list()[-1]
        if date == "No financial reports found yet.":
            raise ProcessLookupError(f"No financial reports from {self.stockcode_url}")
        timestamp = datetime.datetime.strptime(date, "%Y-%m-%d")
        dataframe = self.historical_data_1D(
            stimestamp=int((timestamp - datetime.timedelta(days=30)).timestamp()),
            etimestamp=int((timestamp + datetime.timedelta(days=360)).timestamp()),
        )
        date = dataframe["d"].iloc[-1].to_pydatetime().date()
        return date
