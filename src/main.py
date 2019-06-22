import http.server, socket
import argparse
import handler
import logging, sys
from logging import config

config.fileConfig('logs/logging.cfg')
logger = logging.getLogger('proxy')
sh = logging.StreamHandler()
logger.addHandler(sh)

HOST, PORT = "localhost", 8080
MAX_CONN = 5
BUFFER_SIZE = 1024

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--blacklist', dest='blacklist', help='a black'
                        'list file containing blocked hosts.',
                        default='blacklist.txt')
    parser.add_argument('--whitelist', dest='whitelist', help='a white'
                        'list file containing allowed hosts.',
                        default='whitelist.txt')
    args = parser.parse_args()
    blacklist = [line.rstrip('\n') for line in
                 open(args.blacklist).readlines()]
    logger.info("Blacklisted domains: " + str(blacklist))
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind((HOST, PORT))
            sock.listen(MAX_CONN)
            logger.info("Initializing sockets...")
            logger.info("Sockets binded successfully.")
            logger.info("Server started @ %s:%s", HOST, PORT)
            while True:
                try:
                    conn, addr = sock.accept()
                    data = conn.recv(BUFFER_SIZE)
                    domain = handler.get_host(data)
                    if filter(blacklist, domain):
                        conn.close()
                        logger.warn('A domain was blocked, domain: %s', domain)
                    print(data.decode('ascii'))
                except KeyboardInterrupt:
                    logger.info("Finalizing connection...")
                    sys.exit(0)
        sock.close()
        logger.info("Connection closed.")
        sys.exit(1)
    except Exception as e:
        logger.error("Unable to initialize socket,", e)
        sys.exit(2)
