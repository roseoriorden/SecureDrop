import socket
import os
import json
import sys
import threading
import broadcast
import time
import ssl
import certificate_authority
import requests
from contacts import decrypt_contacts
from base64 import b64encode, b64decode

def init(email, filepath):
    # first check that the contact exists
    contact_exists = False
    contact_is_online = False
    accept_transfer = False
    contacts = decrypt_contacts()
    for contact in contacts:
        if contact["email_address"] == email:
            contact_exists = True
            break
    if not contact_exists:
        print("Contact is not registered.\nExiting file transfer.")
        sys.exit()
    else:
        print('Contact is registered.')
    # then check that filepath exists
    if not os.path.exists(filepath):
        print(filepath + ": No such file or directory.\nExiting file transfer.")
        sys.exit()
    else:
        print('Filepath is registered')
    # then check that contact is online
    
    # get IP from dictionary
    time.sleep(2)
    contacts_dict = broadcast.return_contacts_dict()
    if email in contacts_dict:
        contact_is_online = True
    if not contact_is_online:
        print('Contact is not online')
        try:
            sys.exit()
        except:
            print('Could not exit')
    else:
        ip_addr = contacts_dict[email]
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
    
    # TLS
    # cntx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    cntx = ssl._create_unverified_context()
    # try:
    #cntx.load_cert_chain('./selfsigned.cert', './private.key')
    cntx.load_cert_chain('cert.pem', 'private.key')
    #except:
        #print('no cert/key files found')
        #tcp_server.close()
        #sys.exit()
    s_tcp_server = cntx.wrap_socket(tcp_server, server_side=True)

    s_tcp_server.bind((broadcast.get_ip(),5010)) #Bind to localhost for testing, replace with get_ip() in production
    s_tcp_server.listen(5)
    print('Started TCP Server on ', broadcast.get_ip())
    return s_tcp_server

def init_tcp_client_socket(IP):
    tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # TLS
    # os.environ['REQUESTS_CA_BUNDLE'] = '$(pwd)/cert.pem'
    
    # cntx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    cntx = ssl._create_unverified_context()
    cntx.load_verify_locations('cert.pem')
    cntx.load_cert_chain('cert.pem', 'private.key')
    s_tcp_client = cntx.wrap_socket(tcp_client, server_hostname='securedrop')
    print('Secure TCP client initialized')
    
    s_tcp_client.connect((IP, 5010))
    print('Started TCP Client...')
    return s_tcp_client


def serve_tcp(socket):
    while True:
        client, addr = socket.accept()
        threading.Thread(target=validate_payload, args=(client,addr),daemon=True).start()

def validate_payload(client, addr):
    #while True: #Does this need to be a loop?
        # contacts_dict = broadcast.return_contacts_dict()
        # contact_email = contacts_dict[client]
        payload = client.recv(1024)
        accept = ''
        print(payload)
        # print(b64decode(payload))
        payload = client.recv(4096)
        accept = ''
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
        client.close()

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
    filesize = os.path.getsize(filepath)
    with open(filepath, 'rb') as f:
        data = f.read()
    socket.sendall(data)
    # socket.shutdown(socket.SHUT_WR)
    time.sleep(2)
    socket.close()
    print("Transfer complete")

def send_request(socket):
    payload = b64encode(b'requestsd'+broadcast.get_own_hash().encode())
    #while True:
    #print("Sending TCP Payload: " + payload.decode())
    try:
        socket.sendall(payload)
        data = socket.recv(1024)
    except:
        sys.exit(1)
    #print('TCP DATA ', data.decode())

    if data.decode() == '1':
        return True
    else:
        return False

def init_file_tcp_server():
    threading.Thread(target=serve_tcp, args=(init_tcp_server_socket(),),daemon=True).start() #TCP Server

def main(email, filepath):
    init(email, filepath)

if __name__ == "__main__":
    main('student', 'longtest')
