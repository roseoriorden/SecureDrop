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
import broadcast
import time

def init(email, filepath):
    # first check that the contact exists
    contact_exists = False
    contact_is_online = False
    contacts = decrypt_contacts()
    for contact in contacts:
        if contact["email_address"] == email:
            contact_exists = True
            break
    if not contact_exists:
        print("Contact is not registered.\nExiting file transfer.")
        sys.exit()
    else:
        print('contact is registered.')
    # then check that filepath exists
    if not os.path.exists(filepath):
        print(filepath + ": No such file or directory.\nExiting file transfer.")
        sys.exit()
    else:
        print('filepath is registered')
    # then check that contact is online
    
    # get IP from dictionary
    time.sleep(2)
    contacts_dict = broadcast.return_contacts_dict()
    if email in contacts_dict:
        contact_is_online = True
        print('contact is online, searching for IP...')
    if not contact_is_online:
        print('contact is not online')
        try:
            sys.exit()
        except:
            print('could not exit')
    else:
        ip_addr = contacts_dict[email]
        print('contact is online')
    print(ip_addr)
    # init_tcp_client_socket(IP)
    accept_transfer = send_request(init_tcp_client_socket(ip_addr))
    # ask receiver if they would like to receive file

    if accept_transfer:
        send_tcp(init_tcp_client_socket(ip_addr), filepath)
        print("File sent to " + email)
    else:
        print("Recipient declined.\nExiting file transfer.")
        sys.exit()


def receive_file():
    # 
    print("Receiving file")

def init_tcp_server_socket():
    tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcp_server.bind((broadcast.get_ip(),5010)) #Bind to localhost for testing, replace with get_ip() in production
    tcp_server.listen(5)
    print('Started TCP Server on ', broadcast.get_ip())
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
        threading.Thread(target=validate_payload, args=(client,addr),daemon=True).start()

def validate_payload(client, addr):
    #while True: #Does this need to be a loop?
        # contacts_dict = broadcast.return_contacts_dict()
        # contact_email = contacts_dict[client]
        payload = client.recv(4096)
        accept = ''
        # print(b64decode(payload))
        try:
            if b'requestsd' in b64decode(payload):
                decoded_hash = b64decode(payload).decode().replace('requestsd','')
                while (accept != 'y' and accept != 'n' and accept != 'Y' and accept != 'N'):
                    accept = input('Incoming file from ' + broadcast.get_email_from_hash(decoded_hash)
                            + ', would you like to accept? (y/n): ')
                    if accept == 'y' or accept == 'Y':
                        client.send(b'1') if accept else client.send(b'0')
        except:
            data = payload.decode()
            data += recvall(client).decode()
            with open('output', 'w') as outfile:
                outfile.write(data)
        # except:
        #     data = payload
        #     data.append(recvall(client))
        client.close() #Should we close the connection after?


def recvall(sock):
    BUFF_SIZE = 4096
    data = bytearray()
    while True:
        packet = sock.recv(BUFF_SIZE)
        if not packet:  # Important!!
            break
        data.extend(packet)
    return data

def send_tcp(socket, filepath):
    # payload = b64encode(b'securedrop'+get_own_hash().encode())
    #while True:
    # print("Sending TCP Payload: " + payload.decode())
    filesize = os.path.getsize(filepath)
    # progress = tqdm.tqdm(range(filesize), f"Sending {filepath}", 
    #             unit="B", unit_scale=True, unit_divisor=1024)
    with open(filepath, 'rb') as f:
        data = f.read()
    socket.sendall(data)
    # progress.update(len(bytes_read))
    # socket.shutdown(socket.SHUT_WR)
    socket.close()
    print("transfer complete")
    # data = socket.recv(1024)
    # print("Recieved TCP Payload: " + data.decode())

def send_request(socket):
    # own_hash = broadcast.get_own_hash()
    # payload = b64encode(b'requestsd'+own_hash)
    payload = b64encode(b'requestsd'+broadcast.get_own_hash().encode())
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

def init_file_tcp_server():
    threading.Thread(target=serve_tcp, args=(init_tcp_server_socket(),),daemon=True).start() #TCP Server

def main(email, filepath):
    #if email == '':
        #email = "rose"
        #filepath = "rose"
    
    init(email, filepath)

if __name__ == "__main__":
    main('evan1', 'longtest')
