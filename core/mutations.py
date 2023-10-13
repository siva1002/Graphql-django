import graphene
from .getschema import MusicianGet,AlbumGet,User
from .inputschemas import MusicianInputs,AlbumInputs,UserInputs
from django.contrib.auth.models import User
from .models import Musician,Album
from graphql_jwt.decorators import login_required,user_passes_test,superuser_required,permission_required



'''
  
  Mutation is a type of query that is used to modify or change data on the server.
  mutation is used to add or modify  data in the database

'''
class UserCreate(graphene.Mutation):
    user=graphene.Field(User)
    class Argument:
        userdata=UserInputs(required=True)
    @classmethod
    def mutate(self,infor,userdata):
        user=User.objects.create(username=userdata.username)
        user.set_password(userdata.password)
        user.save()
        return UserCreate(user=user)

class MusicianCreate(graphene.Mutation):
    musician=graphene.Field(MusicianGet)
    class Arguments:
        musiciandata = MusicianInputs(required=True)
    
    @classmethod
    @login_required
    @permission_required(perm=['core.add_musician'])
    def mutate(cls,root,info,musiciandata=None):
        mus=Musician.objects.create(first_name=musiciandata.first_name,last_name=musiciandata.last_name,instrument=musiciandata.instrument)
        if musiciandata.albumname:
            Album.objects.create(artist=mus,name=musiciandata.albumname)
        return MusicianCreate(musician=mus)
    
    
class AlbumCreate(graphene.Mutation):
    album=graphene.Field(AlbumGet)
    class Arguments:
        albumdata=AlbumInputs(required=True)
        
    
    @classmethod
    def mutate(cls,root,info,albumdata):
        mus=Musician.objects.get(pk=albumdata.artist)
        stars=albumdata.numstars if albumdata.numstars else 0
        album= Album.objects.create(artist=mus,name=albumdata.albumname,num_stars=stars)
        return AlbumCreate(album=album)
    
class MusicianDelete(graphene.Mutation):
    artist=graphene.Field(MusicianGet)
    class Arguments:
         artist=graphene.ID(required=True)
    
    @classmethod
    def mutate(cls,root,info,artist):
        musician=Musician.objects.get(pk=artist)
        musician.delete()
        return MusicianDelete(artist=musician)


class AlbumDelete(graphene.Mutation):
    album=graphene.Field(AlbumGet)
    class Arguments:
         album=graphene.ID(required=True)
    
    @classmethod
    def mutate(cls,root,info,album):
        album=Album.objects.get(pk=album)
        album.delete()
        return AlbumDelete(album=album)
    
class AlbumEdit(graphene.Mutation):
    album=graphene.Field(AlbumGet)

    class Arguments:
         album=graphene.ID(required=True)
         album_name=graphene.String(required=True)
         release_date = graphene.Date(required=True)
         num_stars = graphene.Int()

    @classmethod
    def mutate(cls,root,info,album,album_name,release_date,num_stars):
        album=Album.objects.get(pk=album)
        album.name=album_name
        album.release_date=release_date
        album.num_stars=num_stars
        album.save()
        return AlbumEdit(album=album)

class MusicianEdit(graphene.Mutation):
    musician=graphene.Field(MusicianGet)
    class Arguments:
         artist=graphene.ID(required=True)
         first_name=graphene.String(required=True)
         last_name= graphene.String(required=True)

    @classmethod
    def mutate(cls,root,info,artist,first_name,last_name):
        musician=Musician.objects.get(pk=artist)
        musician.first_name=first_name
        musician.last_name=last_name
        musician.save()
        return MusicianEdit(musician)

