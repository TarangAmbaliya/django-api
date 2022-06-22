import random

import graphene
from graphql.error.located_error import GraphQLLocatedError

from api.email import send_welcome_email, send_otp_email
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
    def mutate(root, info, **kwargs):

        username = kwargs.get('username')
        email = kwargs.get('email')
        password = kwargs.get('password')

        try:
            user = UserData.objects.create_user(username=username, email=email, password=password)
        except GraphQLLocatedError:
            return CreateUser(status='Username already exists')
        user.save()

        if send_welcome_email(name=user.username, email=user.email):
            return CreateUser(status='success')
        else:
            return CreateUser(status='email failed')


class ResetPassword(graphene.Mutation):
    """
    This Mutation resets the password.
    """

    class Arguments:
        email = graphene.String()
        password = graphene.String()
        otp = graphene.String()

    status = graphene.String()

    @staticmethod
    def mutate(root, info, **kwargs):

        email = kwargs.get('email')
        password = kwargs.get('password')
        otp = int(kwargs.get('otp'))

        if info.context.user.is_authenticated:
            user = UserData.objects.get(email=email)
            if user.otp == otp:
                if user:
                    if not user.check_password(raw_password=password):
                        user.set_password(raw_password=password)
                    else:
                        return ResetPassword(status='Same as previous password.')
                    user.save()
                else:
                    return ResetPassword(status='No User Found')
            else:
                return ResetPassword(status='Invalid OTP')
        else:
            return ResetPassword(status='You are not authenticated.')
        return ResetPassword(status='success')


class GetOtp(graphene.Mutation):
    class Arguments:
        email = graphene.String()
        password = graphene.String()

    status = graphene.String()

    @staticmethod
    def mutate(root, info, **kwargs):

        email = kwargs.get('email')
        password = kwargs.get('password')

        if info.context.user.is_authenticated:
            user = UserData.objects.get(email=email)
            user.otp = random.randrange(start=111111, stop=999999)
            user.save()
            if user.check_password(password):
                if send_otp_email(name=user.username, email=user.email, otp=user.otp):
                    return GetOtp(status='success')
            else:
                return GetOtp(status='Invalid Password')
        else:
            return GetOtp(status='Not authenticated')
