from rest_framework import viewsets, permissions
from .models import Post, Category
from .serializers import PostListSerializer, PostDetailSerializer, CategorySerializer

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class PostViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Post.objects.filter(status='published')
    serializer_class = PostListSerializer
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return PostDetailSerializer
        return PostListSerializer