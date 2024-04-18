from rest_framework.routers import DefaultRouter

from . import views


app_name = 'events'
router = DefaultRouter(trailing_slash=False)

router.register('location', views.LocationViewSet, basename='location')
router.register('event', views.EventViewSet, basename='event')
router.register('role', views.RoleViewSet, basename='role')
router.register('event-contact', views.EventContactViewSet,
                basename='event-contact')
router.register('social-media', views.SocialMediaViewSet,
                basename='social-media')

urlpatterns = router.urls
