# Xmpp Client :flushed:
 
Project #2 for "Redes" class.
Gustavo De Leon 17085

## Getting Started  

For this projet you will need the following requisites:

### Prerequisites
- python3
- pip3

### Installation

1. Clone the repo  
             
       git clone https://github.com/github_username/repo_name.git
 
2. Install Requirements

       pip install pyasn1==0.3.6 pyasn1-modules==0.1.5 sleekxmpp==1.3.3
 ### Executing
       python ./chat
       
 ## Functionalities
 After running the .py file you will face a menu with 3 options
 1. Sign up
 2. Log in
 0. Exit
 
- Register a new account.
   - Press number 1 
     - This will display you an input for yor new user(id), it is not necessary to write the server extension "@redes2020.xyz" because it is already in the input,
     - After that you have to write your new password.
     - If everything is ok you should see a message like this *Account created for user@redes2020.xyz!*
     - If not you will see *Could not register account*, you should try with another user and password
- Log in. 
   - Press number 2 
     - This will display you an input for yor user(id), it is not necessary to write the server extension "@redes2020.xyz" because it is already in the input,
     - After that you have to write your password.
     - If everything is ok you should see the logged in menu
     
 After logging in you will see a new menu: 
 
0. Log out
1. Establish presence
2. Add a new contact.  
3. Delete my account.
4. Send message to a user.  
5. Show all users
6. Show a specific user.
7. Join to a room.
8. Send messages in a room.
9. Show your contacts
10. Create a room.
11. Send .png files.  
 
- Log out.  
   - Press number 0 
     - This will return you to the previous menu.
- Establish presence.  
   - Press number 1
     - This will ask you for your new status, you can put what ever you want
     - This will ask you for your new status, you can chat, dnd, xa, away.
- Add a new contact.  
   - Press number 2
     - This will ask you for the jid of the user.
     - It is not necessary to write the server extension "@redes2020.xyz"
- Delete my account.  
   - Press number 3
     - This will return you to the previous menu and delete your account.
- Send message to a user.  
   - Press number 4
     - This will ask you for the jid of the user and will print everyone who has that jid.
     - It is not necessary to write the server extension "@redes2020.xyz"
     - Next you have to send your message
- Show all users.
   - Press number 5
     - This will print you all the users registered in redes2020.xyz.
- Show a specific user. 
   - Press number 6
     - This will ask you for the jid of the user and will print everyone who has that jid.
     - It is not necessary to write the complete jid to find the user.
     - It is not necessary to write the server extension "@redes2020.xyz"
- Join to a room.
   - Press number 7
     - This will ask you for the room's name
     - It is not necessary to write the server extension "@conference.redes2020.xyz".
     - Next you have to assign you you nickname.
- Send messages in a room.
   - Press number 8
     - This will ask you for the room's name
     - It is not necessary to write the server extension "@conference.redes2020.xyz".
     - Next you have to send your message
- Show your contacts
   - Press number 9
     - This will print you all the users that you have in your roster and their status.
- Create a room.
   - Press number 10
     - This will ask you for the name of the new room.
     - It is not necessary to write the server extension "@conference.redes2020.xyz".
     - Next you have to assign you you nickname.
     - You will be the owner of the group.
- Send .png files.  
   - Press number 11
     - You will send the png image that is load in this repository called **a.png**
   -You can receive png files too if they are decoded in base64.
   
- Get notifications.  
   - This will happen in the next cases:
     - If you receive a private message
     - If someone joins to a room that you are in
     - If someone says your name in a room message
   
## Documentation and Special Thanks to:
- https://sleekxmpp.readthedocs.io/en/latest/getting_started/muc.html
- https://github.com/fritzy/SleekXMPP/blob/develop/examples/roster_browser.py
- https://github.com/fritzy/SleekXMPP/blob/develop/examples/echo_client.py
- https://xmpp.org/extensions/xep-0045.html#createroom
- XMPP - The definitive guide
- Dieter de Wit
- Vinicio Paz 
And every friend who had the same problem as me and helped me to fix it
     
