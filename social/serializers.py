from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Profile, Post, Comment, Like, Follow


class UserPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username',)


class ProfileSerializer(serializers.ModelSerializer):
    user = UserPublicSerializer(read_only=True)


    class Meta:
        model = Profile
        fields = ('id', 'user', 'bio', 'avatar')


class PostSerializer(serializers.ModelSerializer):
    author = UserPublicSerializer(read_only=True)
    likes_count = serializers.IntegerField(source='likes.count', read_only=True)
    is_liked = serializers.SerializerMethodField()


    class Meta:
        model = Post
        fields = ('id', 'author', 'image', 'caption', 'created_at', 'likes_count', 'is_liked')
        read_only_fields = ('id', 'author', 'created_at', 'likes_count', 'is_liked')


    def get_is_liked(self, obj):
        user = self.context['request'].user
        if not user.is_authenticated:
            return False
        return obj.likes.filter(user=user).exists()


    def create(self, validated_data):
        request = self.context['request']
        return Post.objects.create(author=request.user, **validated_data)


class CommentSerializer(serializers.ModelSerializer):
    author = UserPublicSerializer(read_only=True)


class Meta:
    model = Comment
    fields = ('id', 'author', 'post', 'text', 'created_at')
    read_o