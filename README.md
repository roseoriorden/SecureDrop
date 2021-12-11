Secure Drop

Mustapha Ayad, Sean Cox, Rose O'Riorden, Evan Soroken

The purpose of Secure Drop is to create a secure file transfer protocol between users. We used Python for this project since it offers support for cryptographic libraries such as PyCrypto. 


For each client that runs SecureDrop, the program will check to see if a user is registered. If no user is registered, then a user can register with their full name, email, and create a password. The user info is stored in a JSON file. 

The next time the user runs SecureDrop, they will be prompted to login with the information they entered during registration. Upon logging in, they can add contacts with the command "add". The JSON file is encrypted using AES by generating a new AES128 key. The EAX mode ensures integrity because a ValueError exception will be raised if an attacker tries to change the data. 

A user can use the command "list" to display contact information if the user has added them as a contact, the contact has also added the user as their contact, and the contact is also online on the same network. A UDP connection broadcasts to show and listen if a user is online. Once two users are determined to be online, a TCP connection opens up to determine if the users are in each other's contact list.

A user can use the command "send" to securely transfer their file to their contact over TCP. The user specifies the contact email and the filepath of the file they wish to send.

To exit SecureDrop, the user can use the command "exit". 
