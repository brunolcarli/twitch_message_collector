import requests
import graphene
from artopendoragon.models import ChatMessage

LISA = 'http://104.237.1.145:2154/graphql/'


class ChatMessageType(graphene.ObjectType):
    message_datetime = graphene.DateTime()
    username = graphene.String()
    message = graphene.String()
    message_sentiment = graphene.Float()
    message_offense_level = graphene.Float()    

    def resolve_message_sentiment(self, info, **kwargs):
        payload = f'query{{sentimentExtraction(text: "{self.message}")}}'
        response = requests.post(LISA, json={'query': payload}).json()
        return response['data']['sentimentExtraction']

    def resolve_message_offense_level(self, info, **kwargs):
        payload = f'query{{textOffenseLevel(text: "{self.message}"){{average}}}}'
        response = requests.post(LISA, json={'query': payload}).json()
        return response['data']['textOffenseLevel']['averageß']



class Query(graphene.ObjectType):

    version = graphene.String()
    def resolve_version(self, info, **kwargs):
        return '0.0.0'

    chat_messages = graphene.List(ChatMessageType)
    def resolve_chat_messages(self, info, **kwargs):
        return ChatMessage.objects.filter(**kwargs)
