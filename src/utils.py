"""Utilities for string and connection handler.
"""

def get_host(data):
    """Extracts host from requested package.

    :data: TODO
    :returns: TODO

    """

    hostpos = data.find('http://')
    host = data[hostpos+7:]
    host = host[:host.find('/')]
    return host

def filter_content(blacklist, host):
    """Analyse proxy restrictions.

    :blacklist: list of blocked hosts
    :returns: true if allowed, false if blocked

    """
    return host in blacklist
