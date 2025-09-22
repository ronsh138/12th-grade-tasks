import socket
import json
import os


import protocol_f as pjf # protocol json file

port = 10000
host = "127.0.0.1"
ADDR = (host, port)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

current_dic = os.getcwd()



if "__main__" == __name__:
    client_socket.connect(ADDR)
    while 1:
        data = input("write somthing: ")
        if os.path.isfile(current_dic+f"\\"+data):
            message = pjf.ready_message(data, "file")
        elif data == "exit":
            client_socket.send()
            break
        else:
            message = pjf.ready_message(data, "text")
        state = pjf.send_json(client_socket=client_socket,data=message)
        if state == None:
            print("not good")
            break
        
