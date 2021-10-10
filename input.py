import json
import os.path

def users_registered():
    return os.path.exists("/etc/securedrop/user_info.json")

def registration_prompt():
    while True:
        answer = input("Do you want to register a new user (y/n)?")
        if answer not in ('Y', 'y', 'N', 'n'):
            print("Response must be in the form: y/n")
            continue
        else:
            break
    return answer.lower() == 'y'

def main():
    user_info = {}

    # if there are no current users registered, prompt to register
    # will need to check json file to check (not done yet)
    if not(users_registered()):
        print("No users are registered with this client.")

    if registration_prompt():
        user_info["full_name"] = input("Enter Full Name: ").strip().title()
        user_info["email_address"] = input("Enter Email Address: ")
        
        # obviously hash this password later lol
        while True:
            password = input("Enter password: ")
            password2 = input("Re-enter password: ")
            if not(password == password2):
                print("Passwords do not match, try again.")
                continue
            else:
                break
        user_info['password'] = password
    else: exit()
    #for now, not storing this in the correct location as its easier to delete when testing
    with open('user_info.json', 'w') as f:
        json.dump(user_info, f, indent=4)

if __name__ == '__main__':
    main()
