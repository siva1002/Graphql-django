from django.urls import path
from graphene_django.views import GraphQLView
from .schema import schema
from .views import loginpage,logoutview

from graphql_jwt.middleware import JSONWebTokenMiddleware


urlpatterns = [
    path("graphql",GraphQLView.as_view(graphiql=True)),
    path("login",loginpage,name="loginurl"),
    path("logout/",logoutview,name="logouturl"),
]

