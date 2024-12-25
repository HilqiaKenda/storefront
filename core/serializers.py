from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseCurrentUser

class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name']
        
class UserSeriliazer(BaseCurrentUser):
    class Meta(BaseCurrentUser.Meta):
        fields = ['id', 'username', 'first_name', 'last_name']