from rest_framework.serializers import ModelSerializer
from main.models import AccountRequest, Role

class AccountRequestSerializer(ModelSerializer):
    class Meta:
        model = AccountRequest
        fields = ('id', 'username', 'email', 'requested_role', 'status', 'created_at')
        read_only_fields = ('status', 'created_at')