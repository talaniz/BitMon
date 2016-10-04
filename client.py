try:
    import hashlib
    from getpass import getpass
    from requests import get
    from dialog import Dialog
except ImportError:
    print("Not all requirements met! Please install the following packages:\npython3\npython3requests\npythondialog (pip3 install pythondialog)\n")
    exit()
d = Dialog(dialog="dialog")
d.set_background_title("BitMon - Bit-size Monsters!")
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
        code, tag  = d.menu("Welcome to BitMon!", choices = [
            ("1", "Log-in"),
            ("2", "Register"),
            ("3", "Exit")
        ])
        if code != d.OK:
            d.pause("Goodbye!",seconds=3,title="Exiting...")
            exit()
        answer = int(tag)
        if answer == 1: login()
        if answer == 2:
            response = register()
            if "taken" in response:
                d.msgbox(response,title="Sorry!")
            else:
                d.msgbox(response,title="Success!")
                select_starter(user,password)
        if answer == 3:
            d.pause("Goodbye!",title="Exiting...",seconds=3)
            exit()
    else:
        player_info = get_player_info(user)
        money = player_info[1]
        location = player_info[2]
        code, tag = d.menu("Player: {0}\nMoney: {1}\nLocation: {2}\nWhat would you like to do?".format(user,money,location), choices = [
            ("1","Move"),
            ("2","Examine Location"),
            ("3","Check Inventory"),
            ("4","Check Monsters"),
            ("5","Player Search"),
            ("6","Logout")
        ],title="Main Menu")
        if code != d.OK:
            main_menu()
        tag = int(tag)
        if tag != 6:
            d.pause("That feature is not yet available.",title="Sorry!",seconds=2)
            main_menu()
        if tag == 6:
            logout()
            d.msgbox("You have logged out!",title="Goodbye")
            main_menu()

def get_player_info(user):
    response = get(srv + 'getinfo?user={0}'.format(user)).text
    response = response.split(';;')
    return response


def login():
    global user
    global password
    global logged_in
    code, user = d.inputbox("Username:",title="Logging in...")
    if code != d.OK:
        d.pause("Cancelled!",seconds=3)
        main_menu()
    user = user.lower()
    code, password = d.passwordbox("Password:",title="Logging in...",insecure=True)
    if code != d.OK:
        d.pause("Cancelled!",seconds=3)
        main_menu()
    password = password.encode()
    password = hashlib.md5(password).hexdigest()
    response = get(srv + 'login?user={0}&pass={1}&ipaddr={2}'.format(user,password,ipaddr)).text
    if response != "Success!":
        d.msgbox(response,title="Sorry!")
    else:
        logged_in = 1
        d.msgbox(response,title="Logged in!")

def logout():
    global logged_in
    logged_in = 0

def register():
    global user
    global password
    while True:
        code, user = d.inputbox("Username: ",title="Registration")
        if code != d.OK: main_menu()
        user = user.lower()
        if not 6 <= len(user) <= 12 or not user.isalnum():
            d.msgbox("Please choose an alphanumeric username between 6 and 12 characters.")
            continue
        code, password = d.passwordbox("Password: ",title="Registration",insecure=True)
        if code != d.OK: main_menu()
        code, confirm = d.passwordbox("Confirm Password: ",title="Registration",insecure=True)
        if code != d.OK: main_menu()
        if password != confirm:
            d.msgbox("Passwords do not match!")
            continue
        password = hashlib.md5(password.encode()).hexdigest()
        code, email = d.inputbox("Email address: ",title="Registration")
        if code != d.OK: main_menu()
        break
    return get(srv + 'register?user={0}&pass={1}&ipaddr={2}&email={3}'.format(user,password,ipaddr,email)).text

def select_starter(a,b):
    string = srv + '/selectstarter?user={0}&pass={1}&ipaddr={2}&starter='.format(a,b,ipaddr)
    while True:
        code, choice = d.menu("Select a starter:", choices = [
            ("1","Grumsden"),
            ("2","Hermyle"),
            ("3","Yursba")
        ])
        if code != d.OK:
            d.msgbox("You must make a choice!")
            continue
        choice = int(choice)
        if choice == 1:
            code = d.yesno("Type: Earth\nAttack: 15\nDefense: 13\nIs this the one you want?",title="Grumsden")
            if code == d.OK:
                string += "Grumsden"
                break
            else: continue
        if choice == 2:
            code = d.yesno("Type: Wind\nAttack: 17\nDefense: 11\nIs this the one you want?",title="Hermyle")
            if code == d.OK:
                string += "Hermyle"
                break
            else: continue
        if choice == 3:
            code = d.yesno("Type: Life\nAttack: 14\nDefense: 14\nIs this the one you want?",title="Yursba")
            if code == d.OK:
                string += "Yursba"
                break
            else: continue
    response = get(string).text
    d.msgbox(response,title="Congratulations!")

while True:
    main_menu()
