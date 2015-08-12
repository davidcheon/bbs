#!/usr/bin/env python
#!_*_ coding:utf-8 _*_
from twisted.internet import reactor
from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
class MyProtocol(LineReceiver):
    def __init__(self,users):
        self.status=True
        self.users=users
        self.name=None
    def connectionMade(self):
        print 'connection made:',self.transport.client,self.status
        self.sendLine("what's your name?")
    def connectionLost(self, reason):
        print 'connection lost:',self.transport.client,self.users
        if self.users.has_key(self.name):
            self.users.pop(self.name)
    def lineReceived(self, line):
        if self.status:
            self.handle_name(line)
        else:
            self.handle_data(line)
    def handle_name(self,name):
        if self.users.has_key(name):
            self.sendLine(name+' has named')
            return
        self.users[name]=self
        self.status=False
        self.name=name
        self.sendLine('welcome {0}\n'.format(self.name))
    def handle_data(self,data):
        for name,prot in self.users.items():
            if prot!=self:
                prot.sendLine(name+' said:'+data)
class MyFactory(Factory):
    users={}
    def buildProtocol(self, addr):
        return MyProtocol(self.users)
fac=MyFactory()
reactor.listenTCP(12345,fac)
reactor.run()
