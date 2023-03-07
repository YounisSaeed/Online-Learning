from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static
from .api import viewsets 

router = DefaultRouter()
#router.register(r'Course', CourseViewSet, basename='Course')
#router.register(r'Teacher', TeacherViewSet, basename='Teacher')

urlpatterns = [
    
    path('', include(router.urls)),
    path('signup/',viewsets.RegistrationView.as_view(),name='signup'),
    path('login/',viewsets.LoginView.as_view(),name='login'),
    path('logout/',viewsets.LogoutView.as_view(),name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
