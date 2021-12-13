import json
import getpass
import sys
from base64 import b64encode
from Crypto.Hash import SHA256
from Crypto.Protocol.KDF import bcrypt_check

def main():

    with open('user_info.json', 'r') as f:
        user_info = json.loads(f.read())

    while True:
        try:
            email = input("Enter Email Address: ")
            password = getpass.getpass(prompt="Enter Password: ")

            if(user_info['email_address'] == email):
                try:
                    pwd_b64 = b64encode(SHA256.new(password.encode()).digest())
                    bcrypt_check(pwd_b64.decode(), user_info['password'])

                    print("Welcome to Secure Drop.")
                    print("Type \"help\" For Commands.")
                    break
                except ValueError:
                    print("Email and Password Combination Invalid.")
                    continue
            else:
                print("Email and Password Combination Invalid.")
                continue
        except KeyboardInterrupt:
            sys.exit()

if __name__ == '__main__':
    main()
