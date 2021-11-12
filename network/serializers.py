from rest_framework import serializers

from .models import User, Post


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    creation_date = serializers.DateTimeField(source='created', format='%d/%m/%Y')
    last_modified_date = serializers.DateTimeField(source='modified', format="%d/%m/%Y")

    def get_author(self, obj):
        return obj.author.name()

    class Meta:
        model = Post
        fields = ['author', 'content', 'creation_date', 'last_modified_date', 'likes']


class UserSerializer(serializers.ModelSerializer):
    posts = serializers.SerializerMethodField()

    def get_posts(self, obj):
        posts = Post.objects.filter(author=obj)
        serializer = PostSerializer(posts, many=True)
        return serializer.data

    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'posts']
