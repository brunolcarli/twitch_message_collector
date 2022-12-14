import requests
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
    lisa = 'http://104.237.1.145:2154/graphql/'
    
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

            if resp.startswith('PING'):
                sock.send("PONG\n".encode('utf-8'))
                print('Replying ping')
                continue

            if not len(resp):
                continue

            data = resp.split(' :')

            try:
                user = data[0].split('!')[0][1:]
                msg = data[-1].strip().replace('"', '')
            except Exception as err:
                print(str(err))
                continue
            
            if 'tmi.twitch.tv' in user:
                continue
            if '/NAMES list' in msg:
                continue

            # get text polarity and offensivness from LISA
            payload = f'''
            query{{
                sentimentExtraction(text: "{msg}")
                textOffenseLevel(text: "{msg}"){{average}}
            }}
            '''

            response = requests.post(self.lisa, json={'query': payload}).json()
            sentiment = response['data'].get('sentimentExtraction', 0)
            offense = response['data'].get('textOffenseLevel', {}).get('average', 0)


            try:
                chat_message = ChatMessage.objects.create(
                    username=user,
                    message=msg,
                    message_sentiment=sentiment,
                    message_offense_level=offense
                )
                chat_message.save()
                print(f'Saved: {user}: {msg}')
            except Exception as err:
                print(str(err))

            sleep(1)
