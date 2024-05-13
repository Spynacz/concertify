from rest_framework.routers import DefaultRouter

from posts_comments import routers, views


app_name = 'posts_comments'
router = DefaultRouter(trailing_slash=False)
vote_router = routers.VoteRouter(trailing_slash=False)

router.register('post', views.PostViewSet, basename='post')
router.register('comment', views.CommentViewSet, basename='comment')

urlpatterns = router.urls

vote_router.register('post-vote', views.PostVoteViewSet, basename='post-vote')
vote_router.register('comment-vote', views.CommentVoteViewSet,
                     basename='comment-vote')

urlpatterns += vote_router.urls
