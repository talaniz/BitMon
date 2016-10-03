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
global password
password = ''
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
        except ValueError:
            print("Please make a valid, numerical selection!")
            exit()
        if answer == 1: login()
        if answer == 2:
            response = register()
            if "taken" in response:
                print(response)
            else:
                print(response)
                select_starter(user,password)
        if answer == 3:
            print("Goodbye!")
            exit()
        else:
            print("Please make a valid selection from 1-3.")
    else:
         player_info = get_player_info(user)
         money = str(player_info[1])
         location = player_info[2]
         padding = ' ' * (12 - len(user))
         paduser = user + padding
         padding2 = ' ' * (20 - len(location))
         location += padding2
         padding3 = ' ' * (7 - len(money))
         money += padding3
         answer = int(input('''=================================
| {0} | Money: {1} |
+-------------------------------+
|Location: {2} |
+-------------------------------+
|1 - Move Left |2 - Move Right  |
|3 - Move Up   |4 - Move Down   |
|5 - Inventory |6 - Monsterts   |
|7 - Search    |8 - Logout      |
| for players  |                |
+-------------------------------+
Please make a selection: '''.format(paduser,money,location)))
         if answer == 8:
            print("Logging out...")
            logout()
         else:
            print("This feature is coming soon.")


def get_player_info(user):
    response = get(srv + 'getinfo?user={0}'.format(user)).text
    response = response.split(';;')
    return response


def login():
    global user
    global password
    global logged_in
    user = input("Username: ").lower()
    password = getpass("Password: ").encode()
    password = hashlib.md5(password).hexdigest()
    response = get(srv + 'login?user={0}&pass={1}&ipaddr={2}'.format(user,password,ipaddr)).text
    if response != "Success!":
        print(response)
    else:
        logged_in = 1
        print(response)

def logout():
    global logged_in
    logged_in = 0

def register():
    global user
    global password
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
    return get(srv + 'register?user={0}&pass={1}&ipaddr={2}&email={3}'.format(user,password,ipaddr,email)).text

def select_starter(a,b):
    string = srv + '/selectstarter?user={0}&pass={1}&ipaddr={2}&starter='.format(a,b,ipaddr)
    choice = int(input('''
================================================
Name:       | Type:        | Atk:    | Def:    |
------------------------------------------------
[1]Grumsden | Earth        | 15      | 13      |
------------------------------------------------
[2]Hermyle  | Wind         | 17      | 11      |
------------------------------------------------
[3]Yursba   | Life         | 14      | 14      |
================================================
Please make a choice: '''))
    if choice == 1: string += 'Grumsden'
    if choice == 2: string += 'Hermyle'
    if choice == 3: string += 'Yursba'
    response = get(string).text
    print(response)

while True:
    main_menu()
