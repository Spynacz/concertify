from django.urls import path

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
router.register('schedule-item', views.SchedulItemViewSet,
                basename='schedule-item')
router.register('ticket', views.TicketViewSet, basename="ticket")


urlpatterns = router.urls

urlpatterns += [
    path(
        'event/<int:pk>/send-notification',
        views.CreateNotificationView.as_view(),
        name='send-notification'
    )
]
