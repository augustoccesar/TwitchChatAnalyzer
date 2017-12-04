import socket
import time
from threading import Thread

from twitchchatanalyzer.models import Message


class TwitchIRC(Thread):
    def __init__(self, server, port, token, nick, channel, callback):
        Thread.__init__(self)

        self.server = server
        self.port = port
        self.token = token
        self.nick = nick
        self.channel = channel

        self.callback = callback

    def __connect(self):
        self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.irc.connect((self.server, self.port))
        self.irc.send(bytes("PASS %s\r\n" % self.token, "UTF-8"))
        self.irc.send(bytes("NICK %s\r\n" % self.nick, "UTF-8"))
        self.irc.send(bytes("JOIN #%s\r\n" % self.channel, "UTF-8"))

    def run(self):
        self.__connect()
        while True:
            irc_incoming = self.irc.recv(1024)
            msg = irc_incoming.decode('UTF-8').split(' ')
            if msg[0] == "PING":
                self.irc.send(bytes("PONG %s\r\n" % msg[1], "UTF-8"))
            elif msg[1] == 'PRIVMSG':
                username = msg[0][:msg[0].find("!")].replace(":", "")
                text = ' '.join(msg[3:]).replace(':', '', 1).rstrip()

                self.callback(Message(username=username, text=text, time=time.time()))
