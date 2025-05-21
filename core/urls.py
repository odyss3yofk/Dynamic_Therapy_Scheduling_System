from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import login_view, dashboard, logout_view, TherapistRegistrationViewSet, StudentRegistrationViewSet


router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'children', views.ChildViewSet)
router.register(r'therapists', views.TherapistViewSet)
router.register(r'sessions', views.SessionViewSet)
router.register(r'progress', views.TherapyProgressViewSet)
router.register(r'register/therapist',
                TherapistRegistrationViewSet, basename='register-therapist')
router.register(r'register/student', StudentRegistrationViewSet,
                basename='register-student')


urlpatterns = [
    path('login/', login_view, name='login'),
    path('dashboard/', dashboard, name='dashboard'),
    path('logout/', logout_view, name='logout'),
    path('', include(router.urls)),


]
