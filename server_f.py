import socket
import json
import threading
import base64

import protocol_f as pjf # protocol json file

port = 10000
host = "127.0.0.1"
ADDR = (host, port)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(ADDR)


def main(client_socket, addr):
    while 1:
        data = pjf.recv_json(client_socket=client_socket)
        if data is not None:
            pjf.analize_json(data=data, client_socket=client_socket)
        else:
            print(f"client {addr} has disconnected")
            return


if "__main__" == __name__:
    s.listen(5)
    print(f"server listening on {ADDR}")
    client_socket, addr = s.accept()
    print(f"client connected on {addr}")
    t = threading.Thread(target = main, args=(client_socket,addr,))
    t.start()
    t.join()
