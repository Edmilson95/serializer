



'''
O HyperlinkedModelSerializer é uma variação do ModelSerializer que substitui 
chaves primárias por hyperlinks para representar relacionamentos, seguindo os
princípios RESTful de HATEOAS.
'''

#ModelSerializer usa IDs(pk) para relacionamentos
#HyperlinkedModelSerializer usa URLs para relacionamentos
'''
{
  "id": 1,
  "owner": 42  // ID do dono
}

{
  "url": "http://api.example.com/accounts/1/",
  "owner": "http://api.example.com/users/42/"  // URL do recurso relacionado
} 
'''

from django.db import models

class Account(models.Model):
    account_name = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)

class User(models.Model):
    username = models.CharField(max_length=30, unique=True)
    accounts = models.ManyToManyField(Account)

from rest_framework import serializers

class AccountSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Account
        fields = ['url', 'account_name', 'created']

# O que isso gera ->
{
    "url":"http://api.example.com/accounts/1",
    "account_name": "Premium",
    "created": "2025-03-28T14:30:00Z"
}

