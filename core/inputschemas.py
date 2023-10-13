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

class UserInputs(graphene.InputObjectType):
    username=graphene.String(required=True)
    password=graphene.String(required=True)
    confrimpassword=graphene.String(required=True)