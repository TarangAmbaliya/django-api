import graphene
from django.http import HttpRequest
from graphql import GraphQLError

from users.types import UserType
from users.models import UserData
from api.authentication import TokenOps


class CreateUser(graphene.Mutation):
    """
    This Mutation creates a User.
    """

    class Arguments:
        username = graphene.String()
        email = graphene.String()
        password = graphene.String()

    user = graphene.Field(UserType)

    @staticmethod
    def mutate(root, info, username, email, password):
        user = UserData.objects.create(username=username, email=email)
        user.set_password(raw_password=password)
        user.save()
        return CreateUser(user=user)


class ResetPassword(graphene.Mutation):
    """
    This Mutation resets the password.
    """

    class Arguments:
        email = graphene.String()
        password = graphene.String()

    user = graphene.Field(UserType)

    @staticmethod
    def mutate(root, info, email, password):
        if info.context.user.is_authenticated:
            user = UserData.objects.get(email=email)
            if user:
                if not user.check_password(raw_password=password):
                    user.set_password(raw_password=password)
                else:
                    raise GraphQLError("Password cannot be same.")
                user.save()
            else:
                raise GraphQLError("Invalid Data.")
        else:
            raise GraphQLError("Not authenticated.")


class Login(graphene.Mutation):
    """
    This Mutation gives a access token.
    """

    class Arguments:
        email = graphene.String()
        password = graphene.String()

    auth_token = graphene.String()

    @staticmethod
    def mutate(root, info, email, password):
        user = UserData.objects.get(email=email)
        if user:
            if not user.check_password(raw_password=password):
                raise GraphQLError("Wrong Password.")
            else:
                token = TokenOps.cook_token(payload={'username': user.username})
                return Login(auth_token=token)
        else:
            raise GraphQLError("Invalid Data.")
