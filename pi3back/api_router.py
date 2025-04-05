from rest_framework.routers import DefaultRouter

from pi3back.users.api.views import UserViewSet
from pi3back.occurrences.api.views import (
    ClassroomViewSet,
    OccurrenceViewSet
)

router = DefaultRouter()

router.register('users', UserViewSet, basename='users')
router.register('occurrences', OccurrenceViewSet, basename='occurrences')
router.register('classrooms', ClassroomViewSet, basename='classrooms')

app_name = 'api'
urlpatterns = router.urls