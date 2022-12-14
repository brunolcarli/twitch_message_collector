import os
import socket
from time import sleep
from django.core.management.base import BaseCommand
from artopendoragon.models import ChatMessage

class Command(BaseCommand):
    
    server = 'irc.chat.twitch.tv'
    port = 6667
    nickname = 'beelzebrunothewizard'
    token = 'oauth:dxc89qmhlk078xb1epczuo5nx1lksp'
    channel = '#artopendoragon'
    
    def add_arguments(self, parser):
        # parser.add_argument('--name', type=int)
        ...

    def handle(self, *args, **options):
        print('Subscribing to arto channel')
        sock = socket.socket()

        sock.connect((self.server, self.port))
        sock.send(f"PASS {self.token}\n".encode('utf-8'))
        sock.send(f"NICK {self.nickname}\n".encode('utf-8'))
        sock.send(f"JOIN {self.channel}\n".encode('utf-8'))

        while True:
            try:
                resp = sock.recv(65565).decode('utf-8')
            except Exception as err:
                print(str(err))
                print('Reconnecting...')
                sock = socket.socket()
                sock.connect((self.server, self.port))
                sock.send(f"PASS {self.token}\n".encode('utf-8'))
                sock.send(f"NICK {self.nickname}\n".encode('utf-8'))
                sock.send(f"JOIN {self.channel}\n".encode('utf-8'))
                continue

            print(f'Received {resp}')
            if resp.startswith('PING'):
                sock.send("PONG\n".encode('utf-8'))
                print('Replying ping')
                continue

            if not len(resp):
                continue

            data = resp.split()

            try:
                user = data[0].split('!')[0][1:]
                msg = data[-1]
            except Exception as err:
                print(str(err))
                continue
            
            if 'tmi.twitch.tv' in user:
                continue

            if not msg.startswith(':'):
                continue
            
            msg = msg[1:]

            try:
                chat_message = ChatMessage.objects.create(
                    username=user,
                    message=msg
                )
                chat_message.save()
                print(f'Saved: {user}: {msg}')
            except Exception as err:
                print(str(err))

            sleep(1)
