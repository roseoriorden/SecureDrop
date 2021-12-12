#!/usr/bin/env python3

import sys
import registration
import login
import contacts
from broadcast import start_networking, print_online_contacts
import send_file
import os
import certificate_authority

def get_user_input():
    while(action := input()):
            if action == "help":
                options =\
                    """
                    \"add\"\t-> Add a new contact
                    \"list\"\t-> List all online contacts
                    \"send\"\t-> Transfer file to contact
                    \"exit\"\t-> Exit SecureDrop
                    """
                print(options)
            elif action == "add":
                contacts.main();
            elif action == "list":
                print("Current contacts online:")
                print_online_contacts()
            elif action.split()[0] == "send":
                # begin sending packets
                # call send func with arg 1 and 2 which are contact's email and filepath
                send_file.main(action.split()[1], action.split()[2])
                print('initiating file transfer')
            elif action == "exit":
                sys.exit("exit")
            else:
                print("not a valid cmd")



    
def main():
    registration.main()
    login.main()
    if not os.path.exists('selfsigned.crt'):
        certificate_authority.cert_gen()
    start_networking()
    get_user_input()

if __name__ == '__main__':
    main()
