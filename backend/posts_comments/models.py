from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class BasePostCommentModel(models.Model):
    title = models.CharField(_('title'), max_length=150)
    desc = models.CharField(_('description'), max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        abstract = True

    def save(self, force_insert=False, force_update=False,
             using=None, update_fields=None):
        if not self._state.adding:
            self.modified_at = timezone.now()
        super().save(force_insert, force_update, using, update_fields)


class Post(BasePostCommentModel):
    picture = models.ImageField(_('picture'), blank=True, null=True)
    event = models.ForeignKey('events.Event', related_name='posts',
                              on_delete=models.CASCADE)


class Comment(BasePostCommentModel):
    post = models.ForeignKey(Post, related_name='comments',
                             on_delete=models.CASCADE)
    user = models.ForeignKey('users.ConcertifyUser', related_name='comments',
                             on_delete=models.CASCADE)


class PostVote(models.Model):
    post = models.ForeignKey(Post, related_name='votes',
                             on_delete=models.CASCADE)
    user = models.ForeignKey('users.ConcertifyUser', related_name='post_votes',
                             on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['post', 'user'], name='unique_post_user_combination'
            )
        ]


class CommentVote(models.Model):
    comment = models.ForeignKey(Comment, related_name='votes',
                                on_delete=models.CASCADE)
    user = models.ForeignKey(
        'users.ConcertifyUser',
        related_name='comment_votes',
        on_delete=models.CASCADE
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['comment', 'user'],
                name='unique_comment_user_combination'
            )
        ]
