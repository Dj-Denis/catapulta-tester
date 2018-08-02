"""catapulta_tester URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_view
from django.urls import include
from django.urls import path
from rest_framework.documentation import include_docs_urls

from modules.dashboard.views import DashboardView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', DashboardView.as_view(), name="dashboard"),
    path('plan/', include('modules.test_plans.urls')),
    path('case/', include('modules.test_cases.urls')),
    path('tags/', include('modules.tags.urls')),
    path('account/', include('modules.account.urls')),
    path('accounts/login/', auth_view.login, name='login'),
    path('logout/', auth_view.LogoutView.as_view(), name='logout'),
    path('auth/', include('social_django.urls', namespace='social')),
    path('i18n/', include('django.conf.urls.i18n')),
    path('api/', include('modules.api.urls')),
    path('docs/', include_docs_urls(title="Documentation")),
    path('django-rq/', include('django_rq.urls')),
    path('report/', include('modules.report.urls'))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
