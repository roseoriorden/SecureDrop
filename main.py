import sys
import registration
import login
import contacts
from broadcast import start_networking, print_online_contacts
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
                print('Current Contacts Online:')
                print_online_contacts()
            elif action == "send":
                print("send")
            elif action == "exit":
                sys.exit("exit")
            else:
                print("not a valid cmd")



    
def main():
    registration.main()
    login.main()
    start_networking()
    get_user_input()

if __name__ == '__main__':
    main()
