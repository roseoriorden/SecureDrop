import json
import sys
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Hash import SHA256
from blake3 import blake3
import os.path

def decrypt_contacts():
    try:
        with open("user_contacts.json", "rb") as f:
            nonce, tag, ciphertext = [ f.read(x) for x in (16, 16, -1) ]

        cipher = AES.new(get_derived_key(), AES.MODE_EAX, nonce)
        data = cipher.decrypt_and_verify(ciphertext, tag)
       
        return json.loads(data.decode())

    except FileNotFoundError:
        with open('user_contacts.json', 'w') as f:
            contacts_list.append(new_contact)
            json.dump(contacts_list, f, indent=4)

        with open("user_contacts.json", "rb") as f:
            plaintext = f.read()
        
        cipher = AES.new(get_derived_key(), AES.MODE_EAX)
        ciphertext, tag = cipher.encrypt_and_digest(plaintext)

        with open("user_contacts.json", "wb") as f:
            [ f.write(x) for x in (cipher.nonce, tag, ciphertext) ]

        print('Contact Added.')
        
def list():
    print(json.dumps(decrypt_contacts(),indent=4))

def main():
    global new_contact
    global contacts_list

    new_contact = {}
    contacts_list = []

    try:
        new_contact['full_name'] = input("Enter Full Name of contact: ").strip().title()
        new_contact['email_address'] = input("Enter Email Address of contact: ")
        new_contact['email_hash'] = SHA256.new(new_contact['email_address'].encode()).hexdigest()
       
        contacts = decrypt_contacts()

        for contact in contacts:
            if contact['email_address'] == new_contact['email_address']:
                contact.update(new_contact)
                f.seek(0)
                json.dump(contacts, f, indent=4)
                break

        else:
            contacts.append(new_contact)
            f.seek(0)
            json.dump(contacts, f, indent=4)

        print("Contact Added.")

    except KeyboardInterrupt:
        sys.exit()

def get_derived_key():
    try:
        with open('user_info.json', 'r') as f:
            user_info = json.load(f)
        
        key_material = user_info['password']

        with open('/etc/machine-id','r') as f:
            context = f.read()

        return blake3(key_material.encode(), derive_key_context=context).digest()

    except FileNotFoundError as missing_file:
        sys.exit("Could not open file " + missing_file.filename)
        
if __name__ == "__main__":
    main()
    
