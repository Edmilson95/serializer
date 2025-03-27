from rest_framework import serializers

class Event:
    def __init__(self):
        pass

class BlogPostSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100)
    content = serializers.CharField()

# Podemos tbm fazer uma validação personalizada, por exemplo:
    def validate_title(self, value):
        """
        Checar se o post do blog é sobre Django
        """
        if 'django' not in value.lower():
            raise serializers.ValidationError("Blog post is not about Django")
        return value
    
class EventSerializer(serializers.Serializer):
    description = serializers.CharField(max_length=100)
    start = serializers.DateTimeField()
    finish = serializers.DateTimeField()

# Aqui é como o validate_<campo>, porém a diferença é que aqui posso colocar
# mais de um campo na validacao, por exemplo estou usando o campo start e finish.
    def validate(self, data):
        """
        Checar se finish acaba depois de start
        """
        if data['start'] > data['finish']:
            raise serializers.ValidationError("finish deve ser após start")
        return data
    

from rest_framework.validators import UniqueTogetherValidator

class EventSerializer(serializers.Serializer):
    name = serializers.CharField()
    room_number = serializers.ChoiceField(choices=[101,102,103,104])
    date = serializers.DateField()

# Aqui usamos o UniqueTogetherValidator para fazer uma consulta no banco,
# apos a consulta verificamos se ja existe os campos room_number e date, 
# se houver duplicidade, levantará erro.
    class Meta:
        # Cada quarto tem apenas um evento por dia
        validators = [
            UniqueTogetherValidator(
                queryset=Event.objects.all(),
                fields=['room_number', 'date']
            )
        ]

class UserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField(max_length=100)

class CommentSerializer(serializers.Serializer):
    #caso o user seja opcional (pode ser anonimo, precisa estar com o required=False)
    user = UserSerializer(required=False) # podemos usar uma propria class serializadora para outra,
    content = serializers.CharField(max_length=200)
    created = serializers.DateTimeField()