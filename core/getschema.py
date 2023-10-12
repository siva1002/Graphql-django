from graphene_django import DjangoObjectType
from .models import Musician,Album
from django.contrib.auth import get_user_model



'''GraphQl schemas similar to seralizers in REST'''

class MusicianGet(DjangoObjectType):
    class Meta:
        model = Musician
        fields=("id","first_name","last_name")
        
class AlbumGet(DjangoObjectType):
    class Meta:
        model = Album
        fields="__all__"

class User(DjangoObjectType):
    class Meta:
        model=get_user_model()
        exclude=('password',)
        filter_fields = {
            'first_name': ['exact', 'icontains', 'istartswith'],
        }


