"""sis_exercise URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include
from django.urls import path

from rest_framework.routers import DefaultRouter
from api.views import CommonUserQueriesView, LiteratureDocumentViewSet, LiteratureSearchView, OpenAIMetricsView
from sis_exercise.views import IndexRedirectView

router = DefaultRouter()
router.register('api/literature/search', LiteratureDocumentViewSet, basename='api-literature-search',)

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/search/', LiteratureSearchView.as_view(), name='literature-search'),
    path('api/metrics/user-queries/', CommonUserQueriesView.as_view(), name='user-queries'),
    path('api/metrics/openai-performance/', OpenAIMetricsView.as_view(), name='openai-performance'),
] + router.urls
