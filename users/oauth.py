import os
import requests
from rest_framework.generics import CreateAPIView
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from users.serializers import GoogleLoginSerializer

User = get_user_model()

class GoogleLoginAPIView(CreateAPIView):
    serializer_class = GoogleLoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        code = serializer.validated_data['code']

        token_response = requests.post(
            "https://oauth2.googleapis.com/token",
            data ={ 
                'code': code,
                'client_id': os.environ.get('CLIENT_ID'),
                'client_secret': os.environ.get('CLIENT_SECRET'),
                'redirect_uri': "http://localhost:8000/api/v1/users/google-login",
                'grant_type': "authorization_code"
            }
        )

        token_data = token_response.json()
        access_token = token_data.get("access_token")

        if not access_token:
            return Response({'error': 'invalid access token'})
        
        user_info = requests.get(
            "https://www.googleapis.com/oauth2/v3/userinfo",
            params={"alt": "Json"},
            headers={"Authorization": f"Bearer {access_token}"}
        ).json()

        print(f"USER INFO: {user_info}")

        email = user_info["email"]
        first_name = user_info.get("given_name")
        last_name = user_info.get("family_name")
        user, created = User.objects.get_or_create(
            email=email
        )

        if created or not user.first_name or not user.last_name:
            user.first_name = first_name
            user.last_name = last_name
            user.save()

        refresh = RefreshToken.for_user(user)
        refresh["email"] = user.email
        refresh["birthday"]= str(user.birthday) if user.birthday else None

        return Response({
            "acccess": str(refresh.access_token),
            "refresh": str(refresh)
        })