from rest_framework.routers import DefaultRouter

from . import views


app_name = 'events'
router = DefaultRouter(trailing_slash=False)

router.register('event', views.RoleViewSet, basename='event')
router.register('role', views.RoleViewSet, basename='role')

urlpatterns = router.urls
