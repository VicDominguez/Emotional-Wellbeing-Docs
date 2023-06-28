import logging
import string
import sys
from pathlib import Path
from typing import Collection, Dict


def inner_contained_fully_outer(inner: Collection, outer: Collection) -> bool:
    """
    Checks if all elements of inner collection are present in outer collection
    :param inner: Elements to check in outer
    :param outer: Collection that should contain all inner elements
    :return: true if all elements are present, otherwise false
    """
    return all(element in outer for element in inner)


def obtain_logger(name: string):
    """
    Builds a logger that writes on stdout and a file placed in logs' folder
    :param name: Name of the logger
    :return: Logger ready to use
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    standard_output_handler = logging.StreamHandler(sys.stdout)
    file_handler = logging.FileHandler(Path(__file__).parent / "../../logs" / f'{name}.log')

    formatter = logging.Formatter(
        '[%(asctime)s.%(msecs)d]\t  %(name)s - %(levelname)s \t[%(name)s.%(funcName)s:%(lineno)d]\t %(message)s',
        datefmt='%d/%m/%Y %H:%M:%S'
    )

    standard_output_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    logger.addHandler(standard_output_handler)
    logger.addHandler(file_handler)

    return logger


def data_not_empty(data: Dict):
    """
    Check if any of values of data is not an empty list
    :param data: dict to check
    :return: true if any of these values is not empty, false if all values are empty
    """
    values_empty = list(map(lambda values: len(values) > 0, data.values()))
    return any(values_empty)
