# python tcp socket

this easy to use socket library complete with reciving big data and idle reciving

# how to use

first init the class:

```python

import tcp

# __init__(self, buffer = 2048)
# you can change the buffer size now or later
s = sock() 

# changing the buffer size
# s.buffer = 1000

```

## bind socket

using bind socket:

```python

# create_sock(self, mode, ip, port, timeout = 3)
# we need to set the mode -> bind
# add our bind ip and port
s.create_sock("bind","127.0.0.1", 8080)

# the library will convert the list of client ip [<ip>, <source port>] to "<ip>:<source port>"
# or just ignore the convert_ip param to use normal list
conn, ip = s.listenner(convert_ip = True)

# for bind to read data from client we need to add "conn" parameter on read function
# and set it with the connected client connection
#
# read(self, conn = None, idle = 0, timeout = 0.1, decode = False, limit_data = 0)
# idle -> idle read data or client, we can wait for the reciving data from client
# decode -> we can decode the reciving data into string
# limit_data -> set limit of byte data we want to recive
data = s.read(conn = conn)

```
