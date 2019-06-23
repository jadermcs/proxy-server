"""Utilities for string and connection handler.
"""

def get_host(data):
    """Extracts host from requested package.

    :data: TODO
    :returns: TODO

    """
    data = data.decode('ascii')
    hostpos = data.find('Host: ')
    host = data[hostpos+6:]
    host = host[:host.find('\r')]
    return host.split(':')[0]

def filter_content(blacklist, host):
    """Analyse proxy restrictions.

    :blacklist: list of blocked hosts
    :returns: true if allowed, false if blocked

    """
    return host in blacklist
