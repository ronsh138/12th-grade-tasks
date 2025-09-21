import json
import socket
import os
import base64


buf_size = 1024

ack = "{\"type\": \"ack\"}".encode("utf-8")

def recv_json(client_socket):
    size = client_socket.recv(buf_size)
    client_socket.send(ack)
    size = size.decode("utf-8")
    size = json.loads(size)
    size = int(size["size"])

    data = ""
    t_data = ""
    recv_count = 0
    while recv_count<size:
        t_data = client_socket.recv(buf_size)
        if t_data is None:
            return None
        client_socket.send(ack)
        t_data = t_data.decode("utf-8")
        data += t_data
        recv_count += buf_size

    return json.loads(data)


def send_json(client_socket, data):
    size = str(len(data))
    size = {"size": size}
    size = json.dumps(size).encode()
    client_socket.send(size)
    ack_s = client_socket.recv(buf_size)
    if ack_s is None:
        return None

    j_data = json.dumps(data)

    data_to_send = [j_data[i:i + buf_size] for i in range(0, len(j_data), buf_size)]

    for i in data_to_send:
        chunk = i.encode("utf-8")
        client_socket.send(chunk)
        ack_s = client_socket.recv(buf_size)
        if ack_s is None:
            return None

    return True

def analize_json(data, client_socket):
    if data["type"] == "text":
        print(f"from client {client_socket}: {data["data"]}")

    elif data["type"] == "file":
        if not os.path.exists("uploads"):
            os.makedirs("uploads")
        full_path = os.path.join("uploads", data["name"])
        with open(full_path, 'wb') as file_object:
            b64_bytes_to_decode = data["data"].encode('utf-8')
            data = base64.b64decode(b64_bytes_to_decode)
            file_object.write(data)
    return



def ready_file(data):
    with open(data, "rb") as file_to_encode:
        binary_content = file_to_encode.read()
        base64_bytes = base64.b64encode(binary_content)
        encoded_string = base64_bytes.decode('utf-8')
    return encoded_string

def ready_message(data, type):
    if type == "text":
        message = {'type': type, 'data': data}
    else:
        f_content = ready_file(data)
        message = {'type': type, 'name': data, 'data': f_content}
    return message
