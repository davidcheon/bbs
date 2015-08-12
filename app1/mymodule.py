#!/usr/bin/env python
#!_*_ coding:utf-8 _*_
from SocketServer import TCPServer,ThreadingMixIn,StreamRequestHandler
from models import OnlineUser
users=[]
class Server(ThreadingMixIn,TCPServer):pass
class Handler(StreamRequestHandler):
    def handle(self):
        addr=self.request.getpeername()[0]
        user=OnlineUser.objects.filter(ip=addr)
        if user:
            users.append(user)
            #self.wfile.write(users)
            
# server=Server(('192.168.1.106',1234),Handler)
# server.serve_forever()
            
        
