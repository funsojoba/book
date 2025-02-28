from rest_framework.routers import DefaultRouter


from .views import AuthViewSet, UserViewSet

router = DefaultRouter()

router.register(r'auth', AuthViewSet, basename='auth')
router.register(r'user', UserViewSet, basename='user')

urlpatterns = router.urls
