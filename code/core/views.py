from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
    
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token["custom_field"] = "Custom value"

        if user.no_expiry_token:
            token.set_exp(lifetime=None)

        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        user = self.user
        data["user_id"] = user.id
        data["user_first_name"] = user.first_name
        data["user_last_name"] = user.last_name
        data["user_email"] = user.email

        return data


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer