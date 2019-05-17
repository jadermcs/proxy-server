import http.server, socket
import logging, sys

logging.basicConfig(format='[%(levelname)s][%(asctime)s] %(message)s',
                    datefmt='%m/%d/%Y %H:%M:%S', level=logging.DEBUG,
                    filename='logs/connection.log')


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080
    MAX_CONN = 5
    BUFFER_SIZE = 1024

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind((HOST, PORT))
            sock.listen(MAX_CONN)
            logging.info("Initializing sockets...")
            logging.info("Sockets binded successfully.")
            logging.info("Server started @ %s:%s", HOST, PORT)
            while True:
                try:
                    conn, addr = sock.accept()
                    data = conn.recv(BUFFER_SIZE)
                    print(data.decode('ascii'))
                except KeyboardInterrupt:
                    logging.info("Finalizing connection...")
                    break
        sock.close()
        logging.info("Connection closed.")
        sys.exit(1)
    except Exception as e:
        logging.error("Unable to initialize socket,", e)
        sys.exit(2)
