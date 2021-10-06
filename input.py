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
    user_info = {
        # this password will probably be handled and hashed in a separate file
        #"password" : password
    }

    contact_info = {
        #"full_name" : full_name
        #"email_address" : email_address
    }

    json_userinfo = json.dumps(user_info, indent=4)
    json_contactinfo = json.dumps(contact_info, indent=4)

    # if there are no current users registered, prompt to register
    # will need to check json file to check (not done yet)
    if not(users_registered()):
        print("No users are registered with this client.\n")

    if registration_prompt():
        user_info["full_name"] = input("Enter Full Name: ").strip().title()
        user_info["email_address"] = input("Enter Email Address: ")
        
        # obviously hash this password later lol
        password = input("Enter password: ")
        password2 = input("Re-enter password: ")
        if not(password == password2):
            exit()
            user_info['password'] = password
        else: exit()

    with open("user_info.json", "w") as outfile_userinfo:
        outfile_userinput.write(json_userinfo)

    with open("contact.json", "w") as outfile_contactinfo:
        outfile_contactinfo.write(json_contactinfo)

if __name__ == '__main__':
    main()
