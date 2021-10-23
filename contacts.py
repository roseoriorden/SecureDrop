import json
import sys

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

def main():
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
        
if __name__ == "__main__":
    main()
    
