from rest_framework.routers import DefaultRouter

from posts_comments import views


app_name = 'posts_comments'
router = DefaultRouter(trailing_slash=False)

router.register('post', views.PostViewSet, basename='post')
router.register('comment', views.CommentViewSet, basename='comment')
router.register('post-vote', views.PostVoteViewSet, basename='post-vote')
router.register('comment-vote', views.CommentVoteViewSet,
                basename='comment-vote')


urlpatterns = router.urls
