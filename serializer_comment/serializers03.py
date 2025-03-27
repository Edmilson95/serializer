from rest_framework import serializers

class Account:
    def __init__(self):
        pass


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'account_name', 'users', 'created'] # o django automaticamente mapeia os campos do modelo para o serializer
    #   fields = '__all__' inclui todos os campos do modelo
    #   exclude = ['users'] exclui o campo que voce deseja nao expor no serializer
        

    
