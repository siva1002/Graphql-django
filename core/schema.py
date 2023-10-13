import graphene
from .models import Musician,Album
from .getschema import MusicianGet,AlbumGet,User
from .mutations import (MusicianCreate,MusicianDelete,MusicianEdit,
                        AlbumCreate,AlbumDelete,AlbumEdit,UserCreate)
from graphql_jwt.decorators import login_required,superuser_required,permission_required
import graphql_jwt
from django.contrib.auth import get_user_model
from graphene import relay

class UsersQuery(graphene.ObjectType):
    users=graphene.List(User)
    loggedin_user=graphene.Field(User) 
    
    @superuser_required
    def resolve_users(root,info,**kwargs):
        users=get_user_model()
        return users.objects.all()
    
    def resolve_loggedin_user(root,info,**kwargs):
        return info.context.user


class AlbumQuery(graphene.ObjectType):
    album=graphene.List(AlbumGet,id=graphene.Int(required=False))
    
    @login_required
    @permission_required(perm=['core.view_album'])
    def resolve_album(root,info,id=None,**kwargs):
        if id:
            return Album.objects.filter(id=id)
        return Album.objects.all()
    
class MusicianQuery(graphene.ObjectType):
    musician = graphene.List(MusicianGet,id=graphene.Int(required=False))
    class Meta:
        interfaces = (relay.Node, )
    
    @login_required
    @permission_required(perm=['core.view_musician'])
    def resolve_musician(root, info,id=None,**args):
        if id:
            return Musician.objects.filter(id=id)
        return Musician.objects.all()
        


class Mutations(graphene.ObjectType):
    # create_user=UserCreate.Field()

    create_musician=MusicianCreate.Field()
    edit_musician=MusicianEdit.Field()
    delete_musician=MusicianDelete.Field()

    
    create_album=AlbumCreate.Field()
    edit_album=AlbumEdit.Field()
    delete_album=AlbumDelete.Field()
    
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
class Query(UsersQuery,MusicianQuery,AlbumQuery):
    pass

schema = graphene.Schema(query=Query,mutation=Mutations)
