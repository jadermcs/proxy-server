import http.server, socket
import logging, sys
from logging.config import fileConfig

fileConfig('logs/logging.cfg')
logger = logging.getLogger('proxy')
sh = logging.StreamHandler()
logger.addHandler(sh)


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080
    MAX_CONN = 5
    BUFFER_SIZE = 1024

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
                    print(data.decode('ascii'))
                except KeyboardInterrupt:
                    logger.info("Finalizing connection...")
                    break
        sock.close()
        logger.info("Connection closed.")
        sys.exit(1)
    except Exception as e:
        logger.error("Unable to initialize socket,", e)
        sys.exit(2)
