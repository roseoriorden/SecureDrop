import json

user_info = {
    "full_name" : full_name,
    "email_address" : email_address,
    "password" : password
}

contact_info = {
    "full_name" : full_name
    "email_address" : email_address
}

json_userinfo = json.dumps(user_info, indent=4)
json_contactinfo = json.dumps(contact_info, indent=4)

# if there are no current users registered, prompt to register
# will need to check json file to check
if not(users_registered):
    print("No users are registered with this client.\n")
    answer = input("Do you want to register a new user (y/n)?")
    if answer == 'n':
        exit()
    else:
        full_name = input("Enter Full Name: ")
        user_info['full_name'] = full_name
        email_address = input("Enter Email Address: ")
        user_info['email_address'] = email_address
        # obviously hash this password later lol
        password = input("Enter password")
        password2 = input("Re-enter password: ")
        if not(password == password2):
            exit()
        user_info['password'] = password



with open("user_info.json", "w") as outfile_userinfo:
    outfile_userinput.write(json_userinfo)

with open("user_info.json", "w") as outfile_contactinfo:
    outfile_contactinfo.write(json_contactinfo)
