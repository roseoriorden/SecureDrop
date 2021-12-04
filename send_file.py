import socket
import tqdm # progress bars (not needed but fun)
import os

def send_file(dest_ip, dest_port, filepath):
    SEPARATOR = "<SEPARATOR>"
    BUFFER_SIZE = 4096 # send 4096 bytes each time step
    # the ip address or hostname of the server, the receiver
    host = dest_ip
    # the port, let's use 5001
    port = dest_port
    # the name of file we want to send, make sure it exists
    filename = filepath
    # get the file size
    filesize = os.path.getsize(filename)
    # create the client socket
    s = socket.socket()
    print(f"[+] Connecting to {host}:{port}")
    # FIRST ASK RECEIVER IF THEY WANT TO ACCEPT THE FILE!!!
    s.connect((host, port))
    print("[+] Connected.")