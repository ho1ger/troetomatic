#!/home/hk/script/troetomatic/myvenv/bin/python3

import os

path = "/path/to/install/dir"
photodir = os.path.join(path, "images")

server = "https://awesome.server"
user = "user@awesome.mail.server"
passwd = "awesomepassword"

clientcred = os.path.join(path, server.removeprefix("https://") + "-clientcred.secret")
usercred = os.path.join(server.removeprefix("https://") + "-usercred.secret")

width = 1200

# don't post if in debug mode
debug = False
