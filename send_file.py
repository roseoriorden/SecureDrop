import socket
import tqdm # progress bars (not needed but fun)
import os
from os import path
import json
import sys
from contacts import decrypt_contacts
import threading

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
    # FOR NOW I left this as true
    accept_transfer = True
    if accept_transfer:
        send_file('127.0.0.1', 5010, filepath)
        print("File sent to " + email)
    else:
        print("Recipient declined.\nExiting file transfer.")
        sys.exit()


def send_file(dest_ip, dest_port, filepath):
    # SEPARATOR = "<SEPARATOR>"
    # BUFFER_SIZE = 4096 # send 4096 bytes each time step
    # the ip address or hostname of the server, the receiver
    # host = dest_ip
    # the port
    # port = dest_port
    # the name of file we want to send, make sure it exists
    # filename = filepath
    # get the file size
    # filesize = os.path.getsize(filename)
    
    
    
    


    # FIRST ASK RECEIVER IF THEY WANT TO ACCEPT THE FILE!!!

def receive_file():
    # 
    print("Receiving file")

def init_tcp_server_socket():
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
        payload = client.recv(1024)
        if b'securedrop' in b64decode(payload):
            decoded_hash = b64decode(payload).decode().replace('securedrop','')
            client.send(b'1') if check_incoming_hash(decoded_hash) else client.send(b'0')
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
    socket.send_all(data)
    progress.update(len(bytes_read))
    socket.shutdown(socket.SHUT_WR)
    print("transfer complete")
    # data = socket.recv(1024)
    # print("Recieved TCP Payload: " + data.decode())

def main():
    threading.Thread(target=serve_tcp, args=(init_tcp_server_socket()
                        ,filepath)).start() #TCP Server
    init("emma", "main.py")

if __name__ == "__main__":
    main()