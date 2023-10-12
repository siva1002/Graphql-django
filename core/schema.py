import graphene
from .models import Musician,Album
from .getschema import MusicianGet,AlbumGet,User
from .mutations import MusicianCreate,MusicianDelete,AlbumCreate,AlbumDelete
from graphql_jwt.decorators import login_required,superuser_required,permission_required
import graphql_jwt
from django.contrib.auth import get_user_model

class UsersQuery(graphene.ObjectType):
    users=graphene.List(User)
    loggedin_user=graphene.Field(User)
    
    @login_required
    @superuser_required
    def resolve_users(root,info,**kwargs):
        users=get_user_model()
        return users.objects.all()
    
    def resolve_loggedin_user(root,info,**kwargs):
        print(info.context.user.get_user_permissions())
        return info.context.user

class Query(UsersQuery,graphene.ObjectType):
    musician = graphene.Field(MusicianGet,id=graphene.Int())
    album=graphene.List(AlbumGet)

    @login_required
    def resolve_musician(root, info,id):
        return Musician.objects.get(id=id)
    
    @login_required
    # @permission_required(perm=['core.view_musician'])
    def resolve_album(root,info,**kwargs):
        return Album.objects.all()
    
class Mutations(graphene.ObjectType):
    create_musician=MusicianCreate.Field()
    delete_musician=MusicianDelete.Field()
    
    create_album=AlbumCreate.Field()
    delete_album=AlbumDelete.Field()
    
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


schema = graphene.Schema(query=Query,mutation=Mutations)
# users=graphene.Schema(query=UsersQuery)
