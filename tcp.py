import socket

from select import select
from time import time

class sock:
    def __init__(self, buffer = 2048):
        self.__s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__mode = None
        self.__is_connected = None

        self.buffer = buffer
    
    def create_sock(self, mode, ip, port, timeout = 3):
        if self.__mode != None:
            return [False, "SOCKET_ALREADY_CREATED"]

        if type(port) != int:
            return [False, "PORT_REQUIRE_INT"]
        
        if mode == "bind":
            try:
                self.__s.bind((ip, port))
                self.__s.listen()

                self.__mode = mode
                return [True, "SUCCESS_BIND"]
            except socket.error:
                return [False, "FAILED_BIND_SOCKET"]
        elif mode == "connect":
            self.__s.settimeout(timeout)
            try:
                self.__s.connect((ip, port))
                
                self.__mode = mode
                self.__is_connected = True
            except socket.error:
                return [False, "UNSUCCESS_CONNECTION"]
            
            return [True, "CONNECTED"]
        else:
            return [False, "UNKNOWN_MODE"]
    
    def listenner(self, convert_ip = False):
        if self.__mode == None:
            return [False, "SOCKET_NOT_CREATED"]

        if self.__mode != "bind":
            return [False, "LISTENNER_IS_FOR_BIND_MODE"]

        c, i = self.__s.accept()
        if convert_ip:
            return c, f"{i[0]}:{i[1]}"
        return c, i

    def write(self, data, conn = None):
        if self.__mode == None:
            return [False, "SOCKET_NOT_CREATED"]

        if self.__mode == "bind" and conn == None:
            return [False, "CONN_CLI_NOT_PROVIDED"]
        elif self.__mode == "connect" and not self.__is_connected:
            return [False, "SOCKET_NOT_CONNECTED"]

        if type(data) == str:
            data = data.encode("utf-8")
        
        if self.__mode == "bind":
            try:
                conn.send(data)
            except socket.error:
                return [False, "FAILED_SEND_DATA"]
        elif self.__mode == "connect":
            try:
                self.__s.send(data)
            except socket.error:
                return [False, "FAILED_SEND_DATA"]

        return [True, "SENT"]
    
    def read(self, conn = None, idle = 0, timeout = 0.1, decode = False, limit_data = 0):
        if self.__mode == None:
            return [False, "SOCKET_NOT_CREATED"]

        if self.__mode == "bind" and conn == None:
            return [False, "CONN_CLI_NOT_PROVIDED"]
        elif self.__mode == "connect" and not self.__is_connected:
            return [False, "SOCKET_NOT_CONNECTED"]

        data = b""
        c = None

        if self.__mode == "bind":
            c = conn
        elif self.__mode == "connect":
            c = self.__s
        
        c.setblocking(0)
        
        if idle > 0:
            idle_time = time()
            while time() - idle_time < idle:
                try:
                    r = select([c], [], [], timeout)
                
                    if r[0]:
                        data += c.recv(self.buffer)

                    if limit_data > 0 and len(data) >= limit_data:
                        if decode:
                            return [data.decode("utf-8"), "DATA_REACH_LIMIT"]
                        else:
                            return [data, "DATA_REACH_LIMIT"]

                except socket.error:
                    c.setblocking(0)
                    data = data.decode("utf-8")
                    return [False, "ERR_WHILE_RECV", data]
            c.setblocking(1)
            if decode:
                return [data.decode("utf-8")]
            else:
                return [data]
        else:
            while True:
                try:
                    r = select([c], [], [], timeout)
                    
                    if r[0]:
                        data += c.recv(self.buffer)
                    else:
                        break

                    if limit_data > 0 and len(data) >= limit_data:
                        if decode:
                            return [data.decode("utf-8"), "DATA_REACH_LIMIT"]
                        else:
                            return [data, "DATA_REACH_LIMIT"]

                except socket.error:
                    c.setblocking(0)
                    data = data.decode("utf-8")
                    return [False, "ERR_WHILE_RECV", data]
            c.setblocking(1)
            if decode:
                return [data.decode("utf-8")]
            else:
                return [data]
