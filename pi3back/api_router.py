from rest_framework.routers import DefaultRouter

from pi3back.users.api.views import UserViewSet

router = DefaultRouter()

router.register('users', UserViewSet, basename='users')

app_name = 'api'
urlpatterns = router.urls