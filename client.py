from random import randint
import hashlib
from getpass import getpass
from requests import get

#####Auto-updater
print("Checking for updates to the client...")
webver = get(url="https://bitmonga.me/client").text
with open(__file__,'r') as f: curver = f.read()
if curver != webver:
    print("New update found! Installing!")
    with open(__file__,'w') as f: f.write(webver)
    print("Installed! Relaunching...")
    from subprocess import call
    call(['python3',__file__])
    exit()
else: print("No update found!")

ipaddr = get('https://api.ipify.org').text
global logged_in
global user
user = ''
logged_in = 0
srv = 'https://bitmonga.me/'


def main_menu():
    if logged_in == 0:
        try:
            answer = int(input('''======================
| Welcome to Bitmon! |
======================
| 1 - Login          |
----------------------
| 2 - Register       |
----------------------
| 3 - Exit           |
======================
Please make a selection: '''))
        except ValueError: return "Please make a valid, numerical selection!"
        if answer == 1: login()
        if answer == 2: register()
        if answer == 3: exit()
    else:
        player_info = get_player_info(user)
        money = player_info[1]
        answer = int(input('''=================================
| {0}          | Money: {1}     |
+-------------------------------+
|Location: Coming Soon          |
+-------------------------------+
|1 - Move Left |2 - Move Right  |
|3 - Move Up   |4 - Move Down   |
|5 - Inventory |6 - Monsterts   |
|7 - Search    |8 - Logout      |
| for players  |                |
+-------------------------------+
Please make a selection: '''.format(user,money)))
        if answer == 8:
            logout()
        else:
            print("This feature is coming soon.")


def get_player_info(user):
    response = get(srv + 'getinfo?user={0}'.format(user)).text
    response = response.split(';;')
    return response


def login():
    global user
    global logged_in
    user = input("Username: ").lower()
    password = getpass("Password: ").encode()
    password = hashlib.md5(password).hexdigest()
    response = get(srv + 'login?user={0}&pass={1}&ipaddr={2}'.format(user,password,ipaddr)).text
    if "correct" or "is no" in response:
        print(response)
    else:
        logged_in = 1
        print(response)

def register():
    while True:
        user = input("Username: ").lower()
        if not 6 <= len(user) <= 12 or not user.isalnum():
            print("Please choose an alphanumeric username between 6 and 12 characters.")
            continue
        password = getpass("Password: ")
        confirm = getpass("Confirm Password: ")
        if password != confirm:
            print("Passwords do not match!")
            continue
        password = hashlib.md5(password.encode()).hexdigest()
        email = input("Email address: ")
        break
    print(get(srv + 'register?user={0}&pass={1}&ipaddr={2}&email={3}'.format(user,password,ipaddr,email)).text)


while True:
    main_menu()
