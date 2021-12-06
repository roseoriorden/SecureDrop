import socket
import time
import threading
import json
from Crypto.Hash import SHA256
from contacts import decrypt_contacts

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

def get_own_hash():
        with open('user_info.json', 'r') as f:
            user_info = json.load(f)
        return SHA256.new(user_info['email_address'].encode()).hexdigest()

def check_incoming_hash(data):
    contacts = decrypt_contacts()
    
    for contact in contacts:
        print(contact['email_hash'])
        if contact['email_hash'] == data.decode():
            print("Your contact " + contact['full_name'] + " is online!")

def main():

    t1 = threading.Thread(target=broadcaster,args=(init_broadcast_socket(),))
    t2 = threading.Thread(target=receiver,args=(init_client_socket(),))

    t1.start()
    t2.start()

if __name__ == '__main__':
    main()


