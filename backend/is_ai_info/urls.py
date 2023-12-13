from rest_framework.routers import SimpleRouter

from .views import *

router = SimpleRouter()
router.register(r'admin', AdminViewSet)
router.register(r'student', StudentViewSet)
router.register(r'educator', EducatorViewSet)
router.register(r'forum', ForumViewSet)

urlpatterns = router.urls
