import socket
import tqdm # progress bars (not needed but fun)
import os
from os import path
import json
import network
import sys

def init(email, filepath):
    # first check that the contact exists
    contact_exists = False
    with open("user_contacts.json", "r") as f:
        contacts = json.loads(f.read())
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
    if contact_exists:
        network.main()
        network.broadcast_sender(999)
    
    # ask receiver if they would like to receive file
    # FOR NOW I left this as true
    accept_transfer = True
    if accept_transfer:
        # send file
        print("File sent to " + email)
    else:
        print("Recipient declined.\nExiting file transfer.")
        sys.exit()


def send_file(dest_ip, dest_port, filepath):
    SEPARATOR = "<SEPARATOR>"
    BUFFER_SIZE = 4096 # send 4096 bytes each time step
    # the ip address or hostname of the server, the receiver
    host = dest_ip
    # the port
    port = dest_port
    # the name of file we want to send, make sure it exists
    filename = filepath
    # get the file size
    filesize = os.path.getsize(filename)

    # FIRST ASK RECEIVER IF THEY WANT TO ACCEPT THE FILE!!!



def main():
    init("emma", "network.py")

if __name__ == "__main__":
    main()