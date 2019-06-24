#!/usr/bin/env python3
"""Python web proxy with content filter and caching.
"""
import socketserver
import argparse
import sys
import logging
from logging import config
import handler
import utils


config.fileConfig('logs/logging.cfg')
LOGGER = logging.getLogger('proxy')
SH = logging.StreamHandler()
LOGGER.addHandler(SH)

HOST, PORT = "localhost", 8080
MAX_CONN = 5
BUFFER_SIZE = 1024

if __name__ == "__main__":
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument('--black', dest='blacklist', help='blacklist file'
                        ' containing blocked hosts.', default='blacklist.txt')
    PARSER.add_argument('--white', dest='whitelist', help='whitelist file'
                        ' containing allowed hosts.', default='whitelist.txt')
    PARSER.add_argument('--deny', dest='deny', help='list file containing '
                        'denied terms.', default='deny-terms.txt')
    ARGS = PARSER.parse_args()
    BLACKLIST = [line.rstrip('\n') for line in
                 open(ARGS.blacklist).readlines()]
    WHITELIST = [line.rstrip('\n') for line in
                 open(ARGS.whitelist).readlines()]
    DENY      = [line.rstrip('\n') for line in
                 open(ARGS.deny).readlines()]
    LOGGER.debug("Blacklisted domains: %s", str(BLACKLIST))
    server = None
    LOGGER.info("Initializing server...")
    # Create the server, binding to localhost on port 8080
    # server = socketserver.ThreadingTCPServer((HOST, PORT),
    #                                          handler.MyHandler)
    #                       handler.ThreadedTCPRequestHandler)
    server = socketserver.TCPServer((HOST, PORT),
                                    handler.MyHandler)
    try:
        LOGGER.info("Sockets binded successfully.")
        LOGGER.info("Server started @ %s:%s", HOST, PORT)
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()
    except KeyboardInterrupt:
        LOGGER.info("Finalizing connection...")
    finally:
        server.server_close()
    LOGGER.info("Quiting.")
    sys.exit(0)
