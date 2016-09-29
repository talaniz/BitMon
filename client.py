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
logged_in = 0
srv = 'https://bitmonga.me/'


def main_menu():
 global logged_in
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
  else: print("Please make a valid selection from 1 to 3!")
 else: exit()


def login():
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
