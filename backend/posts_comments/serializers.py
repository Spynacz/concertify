from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from django.db.models import Q

from events.serializers import ValidateUserInContextMixin
from posts_comments import models

from events.serializers import NotificationSerializer
from events.models import Role

from users import models as users_models

class VoteMixin:
    def get_vote_count(self, obj):
        return obj.votes.all().count()

    def get_has_voted(self, obj):
        request = self.context.get("request", None)

        if not hasattr(request, "user") or not request.user.is_authenticated:
            return False

        votes = obj.votes.all()
        return votes.filter(user=request.user).exists()


class PostSerializer(VoteMixin,
                     serializers.ModelSerializer):
    vote_count = serializers.SerializerMethodField()
    has_voted = serializers.SerializerMethodField()

    class Meta:
        model = models.Post
        fields = '__all__'
    
    def create(self, validated_data):

        post = models.Post.objects.create(**validated_data)
        users = users_models.ConcertifyUser.objects.filter(
            role__event_id=post.event.id,
            role__name=Role.NameChoice.USER
        )

        template = users_models.Notification(
            title="New post was added related to the event you are participating in.",
            desc=f"""Post was added to '"{post.event.title }"' event.""",
            notification_type=users_models.Notification.TypeChoice.CASUAL
        )

        NotificationSerializer.create_notifications_for_users(template, users)
        return post

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        users = users_models.ConcertifyUser.objects.filter(
            role__event_id=instance.event.id,
            role__name=Role.NameChoice.USER
        )

        template = users_models.Notification(
            title="Post was changed that is related to the event you are participating in.",
            desc=f"""Post with tiltle '"{instance.title}"'  was changed.""",
            notification_type=users_models.Notification.TypeChoice.CASUAL
        )

        NotificationSerializer.create_notifications_for_users(template, users)
        return instance



class CommentSerializer(VoteMixin,
                        ValidateUserInContextMixin,
                        serializers.ModelSerializer):
    vote_count = serializers.SerializerMethodField()
    has_voted = serializers.SerializerMethodField()

    class Meta:
        model = models.Comment
        fields = '__all__'
        extra_kwargs = {'user': {'read_only': True}}

    def validate(self, attrs):
        attrs = super().validate(attrs)
        attrs['user'] = self.context.get('request').user
        return attrs
    
    def create(self, validated_data):

        comment = models.Comment.objects.create(**validated_data)

        users = users_models.ConcertifyUser.objects.filter(
            Q(role__event_id=comment.event.id) & 
            (Q(role__name=Role.NameChoice.MODERATOR) | Q(role__name=Role.NameChoice.OWNER))
        )

        template = users_models.Notification(
            title="Comment was added to post, related to event that you are organizing.",
            desc=f"""Comment was added to '"{comment.event.title}"' post. """,
            notification_type=users_models.Notification.TypeChoice.CASUAL
        )

        NotificationSerializer.create_notifications_for_users(template, users)
        return comment

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        users = users_models.ConcertifyUser.objects.filter(
            Q(role__event_id=instance.event.id) & 
            (Q(role__name=Role.NameChoice.MODERATOR) | Q(role__name=Role.NameChoice.OWNER))
        )

        template = users_models.Notification(
            title="Comment added to post, related to event that you are organizing, was changed.",
            desc=f"""Comment related with event '"{instance.event.title}"' was changed.""",
            notification_type=users_models.Notification.TypeChoice.CASUAL
        )
        
        NotificationSerializer.create_notifications_for_users(template, users)
        return instance


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
