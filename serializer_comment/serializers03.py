from rest_framework import serializers
from django.utils.timesince import timesince
from django.utils.timezone import now


class Account:
    def __init__(self):
        pass


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'account_name', 'users', 'created'] # o django automaticamente mapeia os campos do modelo para o serializer
    #   fields = '__all__' inclui todos os campos do modelo
    #   exclude = ['users'] exclui o campo que voce deseja nao expor no serializer
        
from django.db import models

class Categoria(models.Model):
    nome = models.CharField(max_length=100)

class Evento(models.Model):
    titulo = models.CharField(max_length=100)
    descricao = models.TextField()
    data = models.DateTimeField()
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='eventos')
    criando_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now_add=True)


class EventoSerializer(serializers.ModelSerializer):
    categoria_nome = serializers.CharField(source='categoria.nome', read_only=True) # verifica o relacionamento em Evento e então busca o nome no model Categoria
    tempo_passado = serializers.SerializerMethodField() # campo dinamico somente leitura, é util quando precisa incluir dados personalizados na serializacao que nao vem diretamente do model.
    
    class Meta:
        model = Evento
        fields = ['id', 'titulo', 'descricao', 'data', 'categoria', 'categoria_nome',
                  'tempo_passado', 'criado_em', 'atualizado_em']
        read_only_fields = ['criando_em', 'atualizado_em'] 
        extra_kwargs = {
            'titulo':{'required': True}, #torna o campo obrigatorio
            'descricao':{'min_length': 10} #tamanho mínimo
        }
        depth = 1 #serializa automaticamente relacionamentos com foreignkey, porém não indicado pois eh simples e pode expor campos sensiveis

    def get_tempo_passado(self, obj): # esse metodo vem do serializermethodfield, ele gera o get + nome do campo
        return timesince(obj.criado_em) 
    
    def validate_titulo(self, value):
        if 'evento' not in value.lower(): # apenas exemplo de como usar validação de um campo
            raise serializers.ValidationError("O titulo deve conter a palavra 'evento'")
        return value
    
    def create(self, validated_data):
        #Não faz sentido sobreescrever o create se vc nao alterar o compartamento padrao dele como esta aqui agora!!
        return Evento.objects.create(**validated_data)
    
    def update(self, instance, validated_data):

        if instance.data < now():
            raise serializers.ValidationError("Eventos passados nao podem ser modificados.")
        
        instance.titulo = validated_data.get('titulo', instance.titulo)
        instance.descricao = validated_data.get('descricao', instance.descricao)

        instance.data = validated_data.get('data', instance.data)
        instance.categoria = validated_data.get('categoria', instance.categoria)
        instance.save()
        
        return instance