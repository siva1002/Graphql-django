from django.urls import path
from graphene_django.views import GraphQLView
from .schema import schema

from graphql_jwt.middleware import JSONWebTokenMiddleware


urlpatterns = [
    path("graphql",GraphQLView.as_view(graphiql=True)),
]

