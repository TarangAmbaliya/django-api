import graphene

from users.types import UserType
from users.models import UserData
from users.mutations import CreateUser, ResetPassword, GetOtp


class Query(graphene.ObjectType):
    """
    The User Query, Interact with the UserData Database using this Query.
    """
    users = graphene.List(UserType)

    @staticmethod
    def resolve_users(root, info):
        return UserData.objects.all().order_by('username')


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    reset_password = ResetPassword.Field()
    get_otp = GetOtp.Field()
