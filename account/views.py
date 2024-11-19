from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken

from account.serializers import UserSerializer


class RegistrationView(APIView):
    serializer_class = UserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})

        # Validate user request if it meets the basic requirements for registration
        # Send validation errors if any
        serializer.is_valid(raise_exception=True)

        # Save user to database
        user = serializer.save()

        # Create token for registered user
        token = Token.objects.create(user=user)

        return Response(
            data={
                'token': token.key,
                'user': serializer.data
            },
            status=status.HTTP_201_CREATED
        )


class LoginView(ObtainAuthToken):
    """
    Override post method to send user data along with token.
    """

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response(data={
            'token': token.key,
            'user': UserSerializer(instance=user).data
        })
