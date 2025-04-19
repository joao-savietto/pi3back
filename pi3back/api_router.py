from rest_framework.routers import DefaultRouter

from pi3back.users.api.views import UserViewSet
from pi3back.core.api.views import ApplicantViewSet
from pi3back.core.api.views import SelectionProcessViewSet
from pi3back.core.api.views import ApplicationViewSet

router = DefaultRouter()

router.register('users', UserViewSet, basename='users')
router.register(
    'applicants',
    ApplicantViewSet,
    basename='applicants'
)
router.register(
    'selection-processes',
    SelectionProcessViewSet,
    basename='selection-processes'
)
router.register(
    'applications',
    ApplicationViewSet,
    basename='applications'
)

app_name = 'api'
urlpatterns = router.urls
