import graphene
from artopendoragon.models import ChatMessage


class ChatMessageType(graphene.ObjectType):
    message_datetime = graphene.DateTime()
    username = graphene.String()
    message = graphene.String()
    message_sentiment = graphene.Float()
    message_offense_level = graphene.Float()



class Query(graphene.ObjectType):

    version = graphene.String()
    def resolve_version(self, info, **kwargs):
        return '0.0.0'

    chat_messages = graphene.List(ChatMessageType)
    def resolve_chat_messages(self, info, **kwargs):
        return ChatMessage.objects.filter(**kwargs)
