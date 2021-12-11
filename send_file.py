import socket
import tqdm # progress bars (not needed but fun)
import os
from os import path
import json
import sys
from contacts import decrypt_contacts
import threading
from base64 import b64encode
from base64 import b64decode

def init(email, filepath):
    # first check that the contact exists
    contact_exists = False
    contacts = decrypt_contacts()
    for contact in contacts:
        if contact["email_address"] == email:
            contact_exists = True
    if not contact_exists:
        print("Contact is not registered.\nExiting file transfer.")
        sys.exit()
    # then check that filepath exists
    if not os.path.exists(filepath):
        print(filepath + ": No such file or directory.\nExiting file transfer.")
        sys.exit()

    # then check that contact is online
    if not contact_exists:
        sys.exit()

    
    # ask receiver if they would like to receive file
    accept_transfer = send_request(tcp_server) 

    if accept_transfer:
        send_tcp(tcp_server, filepath)
        print("File sent to " + email)
    else:
        print("Recipient declined.\nExiting file transfer.")
        sys.exit()


def receive_file():
    # 
    print("Receiving file")

def init_tcp_server_socket():
    global tcp_server 
    tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcp_server.bind(('127.0.0.1',5010)) #Bind to localhost for testing, replace with get_ip() in production
    tcp_server.listen(5)
    print('Started TCP Server...')
    return tcp_server

def init_tcp_client_socket(IP):
    tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcp_client.connect((IP, 5010))
    print('Started TCP Client...')
    return tcp_client

def serve_tcp(socket):
    while True:
        client, addr = socket.accept()
        threading.Thread(target=validate_payload, args=(client,addr),).start()

def validate_payload(client, addr):
    #while True: #Does this need to be a loop?
        contact = broadcast.return_contacts_dict[addr]
        payload = client.recv(1024)
        accept = ''
        if b'requestsd' == b64decode(payload):
            if accept != 'y' or accept != 'n' or accept != 'Y' or accept != 'N':
                accept = input('Incoming file from ' + contact + ', would you like to accept? (y/n): ')
                client.send(b'1') if accept else client.send(b'0')
            #client.close() #Should we close the connection after?

def send_tcp(socket, filepath):
    # payload = b64encode(b'securedrop'+get_own_hash().encode())
    #while True:
    # print("Sending TCP Payload: " + payload.decode())
    filesize = os.path.getsize(filepath)
    progress = tqdm.tqdm(range(filesize), f"Sending {filepath}", 
                unit="B", unit_scale=True, unit_divisor=1024)
    with open(filepath, 'rb') as f:
        data = f.read()
    socket.sendall(data)
    progress.update(len(bytes_read))
    socket.shutdown(socket.SHUT_WR)
    print("transfer complete")
    # data = socket.recv(1024)
    # print("Recieved TCP Payload: " + data.decode())

def send_request(socket):
    payload = b64encode(b'requestsd')
    #while True:
    #print("Sending TCP Payload: " + payload.decode())
    socket.sendall(payload)
    data = socket.recv(1024)
    #print('TCP DATA ', data.decode())

    if data.decode() == '1':
        return True
    else:
        return False
        #socket.close()

def main(email, filepath):
    threading.Thread(target=serve_tcp, args=(init_tcp_server_socket()
                        ,)).start() #TCP Server
    if email == '':
        email = "emma"
        filepath = "emma"
    init(email, filepath)

if __name__ == "__main__":
    main("emma", "main.py")
