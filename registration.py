import json
import os.path
import getpass
import sys
from password import *

def users_registered():
    return os.path.exists("user_info.json")

def registration_prompt():
    while True:
        try:
            answer = input("Do you want to register a new user (y/n)? ")
            if answer not in ('Y', 'y', 'N', 'n'):
                print("Response must be in the form: y/n")
                continue
            else:
                break
        except KeyboardInterrupt:
            sys.exit()
    return answer.lower() == 'y'

def main():
    user_info = {}

    if not users_registered():
        print("No users are registered with this client.")
        if not registration_prompt():
            sys.exit('Did not want to register')

        try:
            user_info["full_name"] = input("Enter Full Name: ").strip().title()
            user_info["email_address"] = input("Enter Email Address: ")
        except KeyboardInterrupt:
            sys.exit()

        while True:
            try:
                password = getpass.getpass(prompt="Enter password: ")
                password2 = getpass.getpass(prompt="Re-enter password: ")

                if not(password == password2):
                    print("Passwords do not match, try again.")
                    continue

                if meets_requirements(password):
                    user_info['password'] = salt_and_hash(password)
                    print("\nPasswords Match.")
                    break
                else:
                    print("Password does not meet strength requirements!")
                    continue
            except KeyboardInterrupt:
                sys.exit()
        try:
            with open('user_info.json', 'w') as f:
                json.dump(user_info, f, indent=4)
            print("User Registered.\n")
        except Exception:
            sys.exit("Unable to write to file 'user_info.json'")

if __name__ == '__main__':
    main()
