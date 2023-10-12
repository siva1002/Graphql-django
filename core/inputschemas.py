
import graphene

class MusicianInputs(graphene.InputObjectType):
    first_name=graphene.String(required=True)
    last_name=graphene.String(required=True)
    instrument=graphene.String(required=True)
    albumname=graphene.String()

class AlbumInputs(graphene.InputObjectType):
    artist=graphene.String(required=True)
    albumname=graphene.String(required=True)
    numstars=graphene.Int()
