from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView
from django.contrib.auth import views as auth_views
from app.views import exportar_registros_view
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.redirect_to_login_or_index, name='root'),
    path('users/login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('index/', views.index, name='index'),
    path('exportar_registros/', exportar_registros_view, name='exportar_registros'),
    # Otras URLs
    path('users/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', include('app.urls')),
    path('tests/', include('tests.urls')),
    # Otras URLs del proyecto...
]
