import graphene
from graphql.error.located_error import GraphQLLocatedError

from users.models import UserData


class CreateUser(graphene.Mutation):
    """
    This Mutation creates a User.
    """

    class Arguments:
        username = graphene.String()
        email = graphene.String()
        password = graphene.String()

    status = graphene.String()

    @staticmethod
    def mutate(root, info, username, email, password):
        try:
            user = UserData.objects.create(username=username, email=email)
        except GraphQLLocatedError:
            return CreateUser(status='Username already exists')
        user.set_password(raw_password=password)
        user.save()
        return CreateUser(status='success')


class ResetPassword(graphene.Mutation):
    """
    This Mutation resets the password.
    """

    class Arguments:
        email = graphene.String()
        password = graphene.String()

    status = graphene.String()

    @staticmethod
    def mutate(root, info, email, password):
        user = info.context.user
        if user.is_authenticated:
            user = UserData.objects.get(email=email)
            if user:
                if not user.check_password(raw_password=password):
                    user.set_password(raw_password=password)
                else:
                    return ResetPassword(status='Same as previous password.')
                user.save()
            else:
                return ResetPassword(status='No User Found')
        return ResetPassword(status='You are not authenticated.')
