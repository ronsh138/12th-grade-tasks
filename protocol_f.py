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

    type = client_socket.recv(buf_size)
    client_socket.send(ack)
    type = type.decode("utf-8")
    type = json.loads(type)
    type = type["type"]

    if type == "file":
        name = client_socket.recv(buf_size)
        client_socket.send(ack)
        name = name.decode("utf-8")
        name = json.loads(name)
        name = name["name"]


    data = ""
    t_data = ""
    recv_count = 0
    while recv_count<size:
        t_data = client_socket.recv(buf_size)
        if t_data is None:
            return None
        client_socket.send(ack)
        t_data = t_data.decode("utf-8")
        t_data = json.loads(t_data)
        data += t_data["data"]
        recv_count += buf_size-13

    if type == "file":
        data = {"type": type, "name": name, "data": data}
    else:
        data = {"type": type, "data": data}

    return data


def send_json(client_socket, data):
    
    j_data = json.dumps(data["data"])
    
    size = str(len(j_data))
    size = {"size": size}
    size = json.dumps(size).encode("utf-8")
    client_socket.send(size)
    ack_s = client_socket.recv(buf_size)
    if ack_s is None:
        return None

    type = {"type": data["type"]}
    type = json.dumps(type).encode("utf-8")
    client_socket.send(type)
    ack_s = client_socket.recv(buf_size)
    if ack_s is None:
        return None
    
    if data["type"] == "file":
        name = {"name": data["name"]}
        name = json.dumps(name).encode("utf-8")
        client_socket.send(name)
        ack_s = client_socket.recv(buf_size)
        if ack_s is None:
            return None
        
    data_to_send = list(j_data[i:i + buf_size-13] for i in range(0, len(j_data), buf_size-13))

    for i in data_to_send:
        chunk = i
        chunk = {"data": chunk}
        chunk = json.dumps(chunk).encode("utf-8")
        client_socket.send(chunk)
        ack_s = client_socket.recv(buf_size-13)
        if ack_s is None:
            return None

    return True

def analize_json(data, client_socket):
    if data["type"] == "text":
        text = data["data"]
        print(f"from client: {text}")

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

