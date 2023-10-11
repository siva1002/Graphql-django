import graphene
from graphene_django import DjangoObjectType
from .models import Musician,Album
from django.contrib.auth import get_user_model
from graphql_jwt.decorators import login_required
import graphql_jwt
from graphene import relay


'''GraphQl schemas similar to seralizers in REST'''

class MusicianGet(DjangoObjectType):
    class Meta:
        model = Musician
        fields=("id","first_name","last_name")
        
class AlbumGet(DjangoObjectType):
    class Meta:
        model = Album
        fields="__all__"

class UserGet(DjangoObjectType):
    class Meta:
        model=get_user_model()
        exclude=('password',)


################################


''' Here our querys live '''
class Query(graphene.ObjectType):
    users=graphene.List(UserGet)
    musician = graphene.Field(MusicianGet,id=graphene.Int(),name=graphene.String())
    album=graphene.List(AlbumGet)
    loggedin_user=graphene.Field(UserGet)
    
    @login_required
    def resolve_musician(root, info,id,name):
        return Musician.objects.get(id=id,first_name=name)
    
    @login_required
    def resolve_album(root,info,**kwargs):
        return Album.objects.all()
    
    @login_required
    def resolve_users(root,info,**kwargs):
        users=get_user_model()
        return users.objects.all()
    
    def resolve_loggedin_user(root,info,**kwargs):
        return info.context.user


'''
  
  Mutation is a type of query that is used to modify or change data on the server.
  mutation is used to add or modify  data in the database

'''

class MusicianCreate(graphene.Mutation):
    musician=graphene.Field(MusicianGet)
    class Arguments:
        first_name=graphene.String(required=True)
        last_name=graphene.String(required=True)
        instrument=graphene.String(required=True)
        albumname=graphene.String(required=True)
    
    @classmethod
    def mutate(cls,root,info,first_name,last_name,instrument,albumname):
        mus=Musician.objects.create(first_name=first_name,last_name=last_name,instrument=instrument)
        Album.objects.create(artist=mus,name=albumname)
        return MusicianCreate(musician=mus)
    
    
class AlbumCreate(graphene.Mutation):
    album=graphene.Field(AlbumGet)
    class Arguments:
        artist=graphene.String(required=True)
        albumname=graphene.String(required=True)
    
    @classmethod
    def mutate(cls,root,info,artist,albumname):
        mus=Musician.objects.get(pk=artist)
        Album.objects.create(artist=mus,name=albumname)
        return MusicianCreate(musician=mus)


class Mutations(graphene.ObjectType):
    create_musician=MusicianCreate.Field()
    create_album=AlbumCreate.Field()
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


schema = graphene.Schema(query=Query,mutation=Mutations)
