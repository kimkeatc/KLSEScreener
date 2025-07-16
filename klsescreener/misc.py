#!/usr/bin/env python

# -*- coding: utf-8 -*-

# Import standard libraries
from datetime import datetime
import functools
import logging


def dec_performance(func):
    """Decorator to measure the performance of a function.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        stime = datetime.now()
        args = func(*args, **kwargs)
        etime = datetime.now()
        elapsed_time = etime - stime
        logging.debug(f"Elapsed time {elapsed_time.total_seconds()} seconds on function \"{func.__name__}\".")
        return args
    return wrapper
