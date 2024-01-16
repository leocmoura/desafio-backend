from django.contrib import admin

from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="FilmRank",
      default_version='v1',
      description="Movies catalog and classification.",
      terms_of_service="#",
      contact=openapi.Contact(email="email@email.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include("users.urls")),
    path('movies/', include("movies.urls")),
    path('ranking/', include("ranking.urls")),
    path('notification/', include("notification.urls")),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
