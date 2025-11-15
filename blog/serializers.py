from rest_framework import serializers
from .models import Post, Category, Comment

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class PostListSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    category = serializers.StringRelatedField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'slug', 'author', 'category', 'created_at', 'content']

class PostDetailSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = '__all__'

    def get_comments(self, obj):
        return Comment.objects.filter(post=obj, active=True).values(
            'author__username', 'content', 'created_at'
        )