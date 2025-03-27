import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "comment.settings")

import django
django.setup()

from django.core.management import call_command

from rest_framework import serializers
from datetime import datetime
from rest_framework.renderers import JSONRenderer

import io 
from rest_framework.parsers import JSONParser


# Objeto simples
class Comment:
    def __init__(self, email, content, created=None):
        self.email = email
        self.content = content
        self.created = created or datetime.now()


comment = Comment(email='leila@example.com', content='foo bar')



# *************************************************************************


# Classe que usaremos para serializar e desserializar (serializers.py)
class CommentSerializer(serializers.Serializer):
    email = serializers.EmailField()
    content = serializers.CharField(max_length=200)
    created = serializers.CharField()

# create e update são opcionais. usar dependendo do caso de uso da classe serializadora
    def create(serlf, validated_data):
        return Comment.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.content = validated_data.get('content', instance.content)
        instance.created = validated_data.get('created', instance.created)
        instance.save()
        return instance


# *Serializando um comentario (comment)*
# transformando um objeto em dados nativos do python(DICT)
serializer = CommentSerializer(comment) 
print(f"Dicionario python: {serializer.data}")
# Dicionario python: {'email': 'leila@example.com', 'content': 'foo bar', 'created': '2025-03-27T15:17:10.375877'}



# renderizando os dados nativos do python para JSON
json = JSONRenderer().render(serializer.data)
print(f"JSON: {json}")
# JSON: b'{"email":"leila@example.com","content":"foo bar","created":"2025-03-27T15:17:10.375877"}'



# *******************************************************
# * Desserializando objetos *
#  Primeiro, analisamos um fluxo(stream) em tipos de dados nativos do Python
stream = io.BytesIO(json)
data = JSONParser().parse(stream)


# então restauramos esses tipos de dados nativos em um dicionário de dados validados.
serializer = CommentSerializer(data=data)
serializer.is_valid()
# True


serializer.validated_data
# {'content': 'foo bar', 'email': 'leila@example.com', 'created': datetime.datetime(2025, 03, 22, 16, 20, 09, 822243)}


comment = serializer.save()

# ********************************

# .save() irá criar uma nova instancia, aqui estamos recebendo um json
serializer = CommentSerializer(data=data)

# .save() vai atualizar a instancia já existente de comment, aqui estamos recebendo um json.
serializer = CommentSerializer(comment, data=data)

# Caso queira injetar dados adicionais no ponto dee salvar a instancia, como usuario atual, hora, etc
# esse metodo abaixo será chamado na view
'''serializer.save(owner=request.user)'''

'''
Ao desserializar dados, você sempre precisa chamar is_valid() antes de tentar acessar os dados '
validados ou salvar uma instância de objeto. Se ocorrerem erros de validação, '
a propriedade .errors conterá um dicionário representando as mensagens de erro resultantes. Por exemplo:'
'''
serializer = CommentSerializer(data={'email': 'foobar', 'content': 'baz'})
serializer.is_valid()
# False
serializer.errors
# {'email': ['Enter a valid e-mail address.'], 'created': ['This field is required.']}