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
        extra_kwargs = {'user': {'required': False}}

    def create(self, validated_data):
        post = validated_data.get('post')
        user = self.context.get("request").user

        if models.PostVote.objects.filter(post=post, user=user).exists():
            raise ValidationError("Object with given data already exists")

        return super().create(validated_data)

    def update(self, instance, validated_data):
        post = validated_data.get('post')
        user = self.context.get("request").user
        obj = models.PostVote.objects.filter(post=post, user=user).first()

        if obj and obj != instance:
            raise ValidationError("Object with given data already exists")

        return super().update(instance, validated_data)


class CommentVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CommentVote
        fields = '__all__'

    def create(self, validated_data):
        comment = validated_data.get('post')
        user = self.context.get("request").user

        if models.CommentVote.objects.filter(
                comment=comment, user=user).exists():
            raise ValidationError("Object with given data already exists")

        return super().create(validated_data)

    def update(self, instance, validated_data):
        comment = validated_data.get('comment')
        user = self.context.get("request").user
        obj = models.CommentVote.objects.filter(
            comment=comment, user=user).first()

        if obj and obj != instance:
            raise ValidationError("Object with given data already exists")

        return super().update(instance, validated_data)
