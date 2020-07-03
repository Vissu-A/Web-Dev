from rest_framework import serializers
from Bookstore.models import Author, Book, Publisher


# def namecheck(value):
#     if value.isalnum:
#         raise serializers.ValidationError('Author name cannot contain numbers')
        
    

# General serializer
# class Authorserializer(serializers.Serializer):
#     name = serializers.CharField(max_length=50, validators=[namecheck])
#     email = serializers.EmailField()
#     age = serializers.IntegerField()
    
#     def validate_age(self, value):
#         """
#         Check that the age of author is above 18.
#         """
        
#         if value < 18:
#             raise serializers.ValidationError("Age is less than 18")
#         return value

#     def create(self, validated_data):
#         return Author.objects.create(**validated_data)

#     def update(self, instance, validated_data):
#         instance.name = validated_data.get('name', instance.name)
#         instance.email = validated_data.get('email', instance.email)
#         instance.age = validated_data.get('age', instance.age)
#         instance.save()
#         return instance


class Authorserializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'
        # fields = '__all__'
        # exclude = []


class Bookserializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
        # fields = '__all__'   # '__all__' to include all fields
        # exclude = []                                                                     # fields to exclude
        depth = 1

class Publisherserializer(serializers.ModelSerializer):
    # books = Bookserializer(many=True, read_only=True)
    class Meta:
        model = Publisher
        fields = '__all__'     