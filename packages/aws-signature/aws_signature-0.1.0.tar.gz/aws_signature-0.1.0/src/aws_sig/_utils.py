"""Utility functions for aws signature objects"""

from __future__ import annotations

from urllib.parse import quote as url_encode, urlparse

from aws_sig.exceptions import TypeErrorOL as TypeError


def x_www_form_encode(body: dict, skip_encoding: bool = False) -> str:
    """encodes a dictionary in the x-www-form-urlencoded format

    Args:
        body (dict): the body of a REST API request in a json or
            dictionary format
        skip (str): a series of characters to skip from encoding

    Returns:
        str: a string representation of the x-www-form-urlencoded for
            the dictionary provided
    """

    if body is None:
        return ""

    if skip_encoding:
        result = [f"{str(x)}={str(y)}" for x, y in body.items()]
    else:
        result = [
            f"{url_encode(str(x))}={url_encode(str(y))}"
            for x, y
            in body.items()
        ]

    return "&".join(result)


def sorted_dictionary(dictionary: dict) -> dict:
    """sorts a dictionary by keys

    Args:
        dictionary (dict): the dictionary to sort

    Returns:
        dict: the sorted dictionary
    """
    return {x: dictionary[x] for x in sorted(dictionary.keys())}


def url_parse(url: str) -> dict:
    """parses a url to find scheme, netloc, path and query

    Args:
        url (str): the url to parse

    Returns:
        dict: a dictionary of all the important information of the url
    """

    url = urlparse(url)

    return {
        "scheme": url.scheme,
        "netloc": url.hostname,
        "path": url.path,
        "query": query_parse(url.query),
    }


def query_parse(query_str: str) -> dict:
    """parses a query string to a dictionary form

    Args:
        query_str (str): the query string from the url

    Returns:
        dict: the query in a dictionary form
    """

    if query_str is None or query_str == "":
        return {}

    if not isinstance(query_str, str):
        raise TypeError(str, type(query_str))

    result = {}

    for param in query_str.split('&'):

        if '=' not in param:
            raise ValueError(
                "'=' missing in parameter. Not properly formatted query string"
            )

        elements = param.split('=', maxsplit=1)

        result[elements[0]] = elements[1] if elements[1] != "" else None

    return result
