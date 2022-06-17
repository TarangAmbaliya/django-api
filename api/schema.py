import graphene
from graphene_django import DjangoObjectType

from users.models import UserData


class UserGetSchema(DjangoObjectType):
    class Meta:
        model = UserData
        fields = '__all__'


class UserCreateSchema(graphene.InputObjectType):
    username = graphene.String()
    email = graphene.String()
    password = graphene.String()


class Query(graphene.ObjectType):
    users = graphene.List(UserGetSchema)

    @staticmethod
    def resolve_users(root, info):
        return UserData.objects.all()


class CreateUser(graphene.Mutation):
    class Arguments:
        user_data = UserCreateSchema(required=True)

    user = graphene.Field(UserGetSchema)

    @staticmethod
    def mutate(root, info, data=None):
        user = UserData(username=data.username, email=data.email, password=data.password)
        user.save()
        return CreateUser(user=user)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
