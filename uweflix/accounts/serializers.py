from djoser.serializers import UserCreateSerializer as CreateUser

class UserCreateSerializer(CreateUser):
    class Meta(CreateUser.Meta):
        fields = ("id",
                  "username",
                  "email",
                  "password",
                  "first name",
                  "last name",)