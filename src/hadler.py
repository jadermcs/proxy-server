def conn_string(conn, data, addr):
    """String parser for connection.

    :conn: TODO
    :data: TODO
    :addr: TODO
    :returns: TODO

    """
    try:
        first_line = data.split('\n')[0]
        url = first_list.split()[1]
        http_pos = url.find('://')
        if http_pos == -1:
            temp = url
        else:
            temp = url[(http_pos+3):]

        port_pos = temp.find(':')
        webserver_pos = temp.find('/')
        if webserver_pos == -1:
            webserver_pos = len(temp)
        webserver = ''
        port = -1
        if port_pos == -1 or webserver_pos < port_pos:
            port = 80
            webserver = temp[:webserver_pos]
        else:
            port = int(temp[(port_pos+1):][:webserver_pos-port_pos-1])
            webserver = temp[:port_pos]

        proxy_server(webserver, port, conn, addr, data)

    except Exception as e:
        pass

def proxy_server(webserver, port, conn, data, addr):
    """TODO: Docstring for proxy_server.

    :webserver: TODO
    :port: TODO
    :conn: TODO
    :data: TODO
    :addr: TODO
    :returns: TODO

    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, PORT))
        sock.send(data)
        while True:
            reply = sock.recv(BUFFER_SIZE)
            if len(reply) > 0:
                conn.send(reply)
                dar = float(len(reply))
                dar = dar / BUFFER_SIZE
                dar = '%.3s KB' % str(dar)
                print('req %s %s' % (str(addr[0]), dar))
            else:
                break
        sock.close()
        conn.close()
    except socket.error as (value, message):
        sock.close()
        conn.close()
        sys.exit(1)
