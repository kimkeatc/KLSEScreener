#!/usr/bin/env python

# -*- coding: utf-8 -*-

# Import standard libraries
from urllib.parse import urljoin
import warnings
import logging
import time

# Import third-party libraries
import requests
import pandas

# Import custom script
from .misc import dec_performance

warnings.simplefilter(action="ignore", category=FutureWarning)


class KLSEScreener:

    def __init__(self):
        self.url = "https://www.klsescreener.com/v2"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }

    def fetch_html(self, url: str, match: str = ".+", extract_links: str | None = None) -> list:
        """Fetch html from website.
        """
        logging.debug(f"Fetching html from {url} with match={match} and extract_links={extract_links}")
        response = requests.get(url=url, headers=self.headers)
        response.raise_for_status()
        dataframes = pandas.read_html(io=response.text, match=match, extract_links=extract_links)
        # Post-process dataframes
        for dataframe in dataframes:
            # If all values in a column are NaN, drop the column
            dataframe.dropna(axis=1, how="all", inplace=True)
        return dataframes

    def fetch_json(self, url: str, timeout: int = 10) -> list:
        """Fetch json from website.
        """
        logging.debug(f"Fetching json from {url}.")
        session = requests.Session()
        due_time = time.time() + timeout
        response = session.get(url=url, headers=self.headers)
        while response.status_code == 202:
            time.sleep(1)  # Wait for 1 second before retrying
            response = session.get(url=url, headers=self.headers)
            if time.time() > due_time:
                raise TimeoutError(f"Timeout after {timeout} seconds while fetching data from {url}.")
        session.close()
        dataframe = pandas.DataFrame(data=response.json())
        return dataframe

    @dec_performance
    def screener(self) -> pandas.DataFrame:
        """Get the KLSE Screener data.
        """
        dataframe = self.fetch_html(url=f"{self.url}/screener/quote_results")[0]
        dataframe["Name"] = dataframe["Name"].str.strip("[s]").str.strip()
        return dataframe

    @dec_performance
    def warrant_screener(self) -> pandas.DataFrame:
        """Get the KLSE Warrant Screener data.
        """
        return self.fetch_html(url=f"{self.url}/screener_warrants/quote_results")[0]

    def _post_process_dataframe(self, dataframe_raw: pandas.DataFrame) -> pandas.DataFrame:
        dataframe = pandas.DataFrame()
        # Iterate each column and insert values and links if available
        for (column, _), series in dataframe_raw.items():
            values = series.apply(lambda x: x[0])
            links = series.apply(lambda x: x[1])
            if values.isna().all():
                dataframe[column] = links
            elif links.isna().all():
                dataframe[column] = values
            else:
                dataframe[f"{column}Link"] = links.apply(lambda x: urljoin(self.url, x) if x else "")
                dataframe[column] = values

        # Remove dummy rows
        number_of_columns = len(dataframe.columns)
        rows_to_drop = []
        for index, row in dataframe.iterrows():
            if len(row.unique()) < (0.5 * number_of_columns):
                rows_to_drop.append(index)
        for index in reversed(rows_to_drop):
            dataframe.drop(labels=index, inplace=True)
        # Remove columns that only contain 'View'.
        dataframe = dataframe.loc[:, ~(dataframe.isin(["", "View"])).all()]
        # Reset index
        dataframe.reset_index(inplace=True)
        return dataframe

    @dec_performance
    def recent_dividends(self):
        """Get the recent dividends data.
        """
        dataframe = self.fetch_html(url=f"{self.url}/entitlements/dividends", extract_links="all")[0]
        dataframe = self._post_process_dataframe(dataframe)
        return dataframe

    @dec_performance
    def upcoming_dividends(self):
        """Get the upcoming dividends data.
        """
        dataframe = self.fetch_html(url=f"{self.url}/entitlements/dividends", extract_links="all")[1]
        dataframe = self._post_process_dataframe(dataframe)
        return dataframe

    @dec_performance
    def recent_share_issue(self):
        """Get the recent share issue data.
        """
        dataframe = self.fetch_html(url=f"{self.url}/entitlements/shares-issue", extract_links="all")[0]
        dataframe = self._post_process_dataframe(dataframe)
        return dataframe

    @dec_performance
    def upcoming_share_issue(self):
        """Get the upcoming share issue data.
        """
        dataframe = self.fetch_html(url=f"{self.url}/entitlements/shares-issue", extract_links="all")[1]
        dataframe = self._post_process_dataframe(dataframe)
        return dataframe

    @dec_performance
    def recent_quarterly_reports(self):
        """Get the recent quarterly reports data.
        """
        dataframe = self.fetch_html(url=f"{self.url}/financial-reports", extract_links="all")[0]
        dataframe = self._post_process_dataframe(dataframe)
        return dataframe
