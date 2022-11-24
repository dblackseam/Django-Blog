from django.urls import path

from api.v1.blog import views

# from rest_framework import routers - # Использовалось для работы с ModelViewSet.


# from .views import ArticleListViewSet - # Использовалось для работы с ModelViewSet.

app_name = "blog"

urlpatterns = [
    path("", views.ArticleListView.as_view(), name="list_articles")
]

# Использовалось для работы с ModelViewSet.
# router = routers.DefaultRouter()
#
# router.register('articles', ArticleListViewSet, basename='article')
#
# urlpatterns = [
#     path('', include(router.urls)),
# ]
