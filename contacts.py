import json
import sys
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import scrypt
import os.path


from input import main

def print_contacts(a_key):
    while True:
        try:
            answer = input("Do you want to view contacts (y/n)? ")
            if answer not in ('Y', 'y', 'N', 'n'):
                print("Response must be in the form: y/n")
                continue
            else:
                break
        except KeyboardInterrupt:
            sys.exit()
    if answer:
        file_in = open("encrypted_contacts.txt", "rb")
        nonce, tag, ciphertext = [ file_in.read(x) for x in (16, 16, -1) ]
        cipher = AES.new(a_key, AES.MODE_EAX, nonce)
        data = cipher.decrypt_and_verify(ciphertext, tag)
        print(data)


def contact_prompt():
    while True:
        try:
            answer = input("Do you want to add a new contact (y/n)? ")
            if answer not in ('Y', 'y', 'N', 'n'):
                print("Response must be in the form: y/n")
                continue
            else:
                break
        except KeyboardInterrupt:
            sys.exit()
    return answer.lower() == 'y'

def main_contacts():
    new_contact = {}
    contact_list = {}
    num_of_contacts = 0
    
    while contact_prompt():
        try:
            new_contact["full_name"] = input("Enter Full Name of contact: ").strip().title()
            new_contact["email_address"] = input("Enter Email Address of contact: ")
            contact_list['Contact' + str(num_of_contacts+1)] = { new_contact['full_name']: new_contact['email_address']}
            with open('user_contacts.json', 'w') as f: 
                f.write(json.dumps(contact_list, indent=4))
                print("Contact added. ")
                num_of_contacts = num_of_contacts + 1
        except KeyboardInterrupt:
            sys.exit()

    if os.path.exists("user_info.json"):
        try:
            with open('user_info.json', 'r') as f:
                user_info = json.loads(f.read())
                password = user_info['email_address']
                salt = get_random_bytes(16)
                key = scrypt(password, salt, 16, N=2**14, r=8, p=1)
                file_in = open("user_contacts.json", "rb")
                plaintext = file_in.read()
                cipher = AES.new(key, AES.MODE_EAX)
                ciphertext, tag = cipher.encrypt_and_digest(plaintext)

                file_out = open("encrypted_contacts.txt", "wb")
                [ file_out.write(x) for x in (cipher.nonce, tag, ciphertext) ]
                file_out.close()
                print_contacts(key)
        except Exception:
            sys.exit("Unable to read file 'user_info.json'")
    

    
        
if __name__ == "__main__":
    main()
    main_contacts()
    
