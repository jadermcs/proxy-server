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
    PARSER.add_argument('--blacklist', dest='blacklist', help='a black'
                        'list file containing blocked hosts.',
                        default='blacklist.txt')
    PARSER.add_argument('--whitelist', dest='whitelist', help='a white'
                        'list file containing allowed hosts.',
                        default='whitelist.txt')
    ARGS = PARSER.parse_args()
    BLACKLIST = [line.rstrip('\n') for line in
                 open(ARGS.blacklist).readlines()]
    LOGGER.info("Blacklisted domains: %s", str(BLACKLIST))
    try:
        LOGGER.info("Initializing server...")
        # Create the server, binding to localhost on port 9999
        server = socketserver.ThreadingTCPServer((HOST, PORT),
                              handler.ThreadedTCPRequestHandler)
        LOGGER.info("Sockets binded successfully.")
        LOGGER.info("Server started @ %s:%s", HOST, PORT)
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()
    except KeyboardInterrupt:
        LOGGER.info("Finalizing connection...")
    LOGGER.info("Quiting.")


    #                 # DOMAIN = handler.get_host(DATA)
    #                 # if handler.filter_content(BLACKLIST, DOMAIN):
    #                 #     CONN.send(b'Blocked content.')
    #                 #     CONN.close()
    #                 #     LOGGER.warning('A domain was blocked, domain: %s', DOMAIN)
    #                 print(DATA.decode('ascii'))
    #             except KeyboardInterrupt:
    #                 CONN.close()
    #                 LOGGER.info("Finalizing connection...")
    #                 break
    #     sock.close()
    #     LOGGER.info("Connection closed.")
    #     sys.exit(1)
    # except socket.error as err:
    #     LOGGER.error("Unable to initialize socket, %s", err)
    #     sys.exit(2)
