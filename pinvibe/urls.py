from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from pins.views import PinViewSet, CommentViewSet, LikeViewSet
from boards.views import BoardViewSet
from users.views import FollowViewSet
from django.conf import settings
from django.conf.urls.static import static
from pins.views import CategoryViewSet

router = DefaultRouter()
router.register(r'pins', PinViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'likes', LikeViewSet)
router.register(r'boards', BoardViewSet)
router.register(r'follows', FollowViewSet)
router.register(r'categories', CategoryViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/', include(router.urls)),
    path('api/users/', include('users.urls')),
    path('', include('pins.urls')),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



