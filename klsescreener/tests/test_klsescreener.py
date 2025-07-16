#!/usr/bin/env python

# -*- coding: utf-8 -*-

# Import third-party libraries
import pandas
import pytest

# Import custom script
from ..klsescreener import KLSEScreener


@pytest.fixture
def klsescreener():
    """Fixture to create an instance of KLSEScreener."""
    return KLSEScreener()


def test_screener(klsescreener):
    """Test the screener method."""
    dataframe = klsescreener.screener()
    assert isinstance(dataframe, pandas.DataFrame)
    assert not dataframe.empty
    assert "Name" in dataframe.columns


def test_warrant_screener(klsescreener):
    """Test the warrant_screener method."""
    dataframe = klsescreener.warrant_screener()
    assert isinstance(dataframe, pandas.DataFrame)
    assert not dataframe.empty
    assert "Name" in dataframe.columns


def test_recent_dividends(klsescreener):
    """Test the recent_dividends method."""
    dataframe = klsescreener.recent_dividends()
    assert isinstance(dataframe, pandas.DataFrame)
    assert not dataframe.empty
    assert "Name" in dataframe.columns


def test_upcoming_dividends(klsescreener):
    """Test the upcoming_dividends method."""
    dataframe = klsescreener.upcoming_dividends()
    assert isinstance(dataframe, pandas.DataFrame)
    assert not dataframe.empty
    assert "Name" in dataframe.columns


def test_recent_share_issue(klsescreener):
    """Test the recent_share_issue method."""
    dataframe = klsescreener.recent_share_issue()
    assert isinstance(dataframe, pandas.DataFrame)
    assert not dataframe.empty
    assert "Name" in dataframe.columns


def test_upcoming_share_issue(klsescreener):
    """Test the upcoming_share_issue method."""
    dataframe = klsescreener.upcoming_share_issue()
    assert isinstance(dataframe, pandas.DataFrame)
    assert not dataframe.empty
    assert "Name" in dataframe.columns


def test_recent_quarterly_reports(klsescreener):
    """Test the recent_quarterly_reports method."""
    dataframe = klsescreener.recent_quarterly_reports()
    assert isinstance(dataframe, pandas.DataFrame)
    assert not dataframe.empty
    assert "Name" in dataframe.columns
