from rest_framework.routers import DefaultRouter


from .views import BookViewSet, AdminBookView

router = DefaultRouter()

router.register(r'books', BookViewSet, basename='book')
router.register(r'admin-books', AdminBookView, basename='admin-book')

urlpatterns = router.urls
