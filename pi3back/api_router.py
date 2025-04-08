from rest_framework.routers import DefaultRouter

from pi3back.users.api.views import UserViewSet
from pi3back.core.api.views import ApplicantViewSet

router = DefaultRouter()

router.register('users', UserViewSet, basename='users')
router.register(
    'applicants',
    ApplicantViewSet,
    basename='applicants'
)

app_name = 'api'
urlpatterns = router.urls
