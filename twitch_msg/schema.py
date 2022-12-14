import graphene
import artopendoragon.schema


class Query(artopendoragon.schema.Query, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)
