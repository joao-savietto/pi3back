from rest_framework.routers import DefaultRouter

from pi3back.users.api.views import UserViewSet
from pi3back.core.api.views import LinkedInProfileViewSet

router = DefaultRouter()

router.register('users', UserViewSet, basename='users')
router.register(
    'linkedin-profiles',
    LinkedInProfileViewSet,
    basename='linkedin-profiles'
)

app_name = 'api'
urlpatterns = router.urls
