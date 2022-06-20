from graphene_django.types import DjangoObjectType

from users.models import UserData


class UserType(DjangoObjectType):
    """
    UserType.
    """

    class Meta:
        model = UserData
