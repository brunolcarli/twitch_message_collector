import graphene
from artopendoragon.models import ChatMessage
from artopendoragon.analytics import get_messages_count_rank, get_messages_average_polarities


class ChatMessageType(graphene.ObjectType):
    message_datetime = graphene.DateTime()
    username = graphene.String()
    message = graphene.String()
    message_sentiment = graphene.Float()
    message_offense_level = graphene.Float()


class MessageCountRank(graphene.ObjectType):
    username = graphene.String()
    messages_count = graphene.Int()

    def resolve_username(self, info, **kwargs):
        return self[0]

    def resolve_messages_count(self, info, **kwargs):
        return self[1]


class MessageAveragePolarity(graphene.ObjectType):
    positive = graphene.Float()
    negative = graphene.Float()
    neutral = graphene.Float()


class Query(graphene.ObjectType):

    version = graphene.String()
    def resolve_version(self, info, **kwargs):
        return '0.0.1'

    chat_messages = graphene.List(ChatMessageType)
    def resolve_chat_messages(self, info, **kwargs):
        return ChatMessage.objects.filter(**kwargs)

    top_ten = graphene.List(MessageCountRank)
    def resolve_top_ten(self, info, **kwargs):
        return get_messages_count_rank(ChatMessage.objects.filter(**kwargs))

    message_average_polarity = graphene.Field(MessageAveragePolarity)
    def resolve_message_average_polarity(self, info, **kwargs):
        return get_messages_average_polarities(ChatMessage.objects.filter(**kwargs))
