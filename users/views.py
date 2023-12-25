from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import CustomUserSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from drf_yasg.utils import swagger_auto_schema

class CustomAuthToken(ObtainAuthToken):
    @swagger_auto_schema(
        #request_body=CustomUserSerializer,             
        required=['username', 'password'],
        )
    def post(self, request, *args, **kwargs):
        """Post the users email and password and returns a token that can be used to authenticate on other endpoints
        The token key should be included in the Authorization HTTP header prefixed by the string literal "Token" For example: Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
        """
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': 'token '+token.key,
            'user_id': user.pk,
            'email': user.email
        })