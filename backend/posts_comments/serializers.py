from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from events.serializers import ValidateUserInContextMixin
from posts_comments import models


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Post
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Comment
        fields = '__all__'


class PostVoteSerializer(ValidateUserInContextMixin,
                         serializers.ModelSerializer):
    class Meta:
        model = models.PostVote
        fields = '__all__'
        extra_kwargs = {'user': {'read_only': True}}

    def create(self, validated_data):
        post = validated_data.get('post')
        user = self.context.get("request").user

        if models.PostVote.objects.filter(post=post, user=user).exists():
            raise ValidationError("Object with given data already exists")

        return models.PostVote.objects.create(post=post, user=user)


class CommentVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CommentVote
        fields = '__all__'
        extra_kwargs = {'user': {'read_only': True}}

    def create(self, validated_data):
        comment = validated_data.get('comment')
        user = self.context.get("request").user

        if models.CommentVote.objects.filter(
                comment=comment, user=user).exists():
            raise ValidationError("Object with given data already exists")

        return models.CommentVote.objects.create(
                comment=comment,
                user=user
            )
