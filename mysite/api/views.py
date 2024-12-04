from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from .models import BlogPost
from .serializers import BlogPostSerializer
from rest_framework.views import APIView

class BlogPostListCreate(generics.ListCreateAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer

    # Override any HTTP method, adds delete route (deletes all blog posts)
    def delete(self, request, *args, **kwargs):
        BlogPost.objects.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Access individual post and be able to delete it
class BlogPostRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    lookup_field = "pk"

class BlogPostList(APIView):
    def get(self, request, format=None):
        # Get title from query parameters
        title = request.query_params.get("title", "")

        if title:
            # Filter base on title
            blog_posts = BlogPost.objects.filter(title__icontains=title)
        else:
            # Returns everything if no title found
            blog_posts = BlogPost.objects.alL()

        serializer = BlogPostSerializer(blog_posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)