from rest_framework import serializers
from .models import Blog, Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

# related_name should be used to define the relationship between the two models
# related_name='comments'
class BlogSerializer(serializers.ModelSerializer):
    comments =CommentSerializer(many=True, read_only=True)
    class Meta:
        model = Blog
        fields = '__all__'