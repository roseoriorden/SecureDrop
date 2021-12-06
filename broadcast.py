import socket
import time
import threading
import json
from base64 import b64encode, b64decode
from Crypto.Hash import SHA256
from contacts import decrypt_contacts

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip

def init_broadcast_socket():
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    return server

def init_client_socket():
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    return client

def init_tcp_server_socket():
    tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcp_server.bind((get_ip(),5000))
    tcp_server.listen(5)
    return tcp_server

def init_tcp_client_socket(IP):
    tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcp_client.connect((IP, 5000))
    return tcp_client


def broadcaster(socket):
    while True:
        #print("sent " + get_own_hash())
        socket.sendto(get_own_hash().encode(), ("", 5005))
        time.sleep(1)

def receiver(socket):
    socket.bind(("", 5005))
    while True:
        data, addr = socket.recvfrom(1024)
        check_incoming_hash(data)
#        print("received " + data.decode() + " from " + addr[0])

def serve_tcp(socket):
    client, addr = socket.accept()
    while True:
        payload = client.recv(1024)
        #print(payload.decode())
        if b'securedrop' in b64decode(payload):
            #print(b64decode(payload))
            decoded_hash = b64decode(payload).decode().replace('securedrop','')
            print(decoded_hash)

            client.send(b'1') if check_incoming_hash(decoded_hash) else client.send(b'0')
        else:
            pass
    socket.close()

def send_tcp(socket):
    payload = b64encode(b'securedrop'+get_own_hash().encode())
    while True:
        print("sending payload " + payload.decode())

        socket.sendall(payload)
        data = socket.recv(1024)
        print(data.decode())
        time.sleep(1)
    socket.close()

def get_own_hash():
        with open('user_info.json', 'r') as f:
            user_info = json.load(f)
        return SHA256.new(user_info['email_address'].encode()).hexdigest()

def check_incoming_hash(data):
    contacts = decrypt_contacts()
    
    for contact in contacts:
        #print(contact['email_hash'])
        return contact['email_hash'] == data
            #print("Your contact " + contact['full_name'] + " is online!")

def main():
    
    t1 = threading.Thread(target=broadcaster,args=(init_broadcast_socket(),))
    t2 = threading.Thread(target=receiver,args=(init_client_socket(),))

    t1 = threading.Thread(target=serve_tcp, args=(init_tcp_server_socket(),))
    t2 = threading.Thread(target=send_tcp, args=(init_tcp_client_socket(get_ip()),)) #BROADCASTERS IP?


    t1.start()
    t2.start()

if __name__ == '__main__':
    main()


