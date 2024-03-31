from rest_framework import serializers

from posts_comments import models


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Post
        field = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Comment
        field = '__all__'


class PostVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PostVote
        field = '__all__'


class CommentVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CommentVote
        fields = '__all__'
