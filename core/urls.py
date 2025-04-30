from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('', views.home_view, name='home'),
    path('track-mood/', views.track_mood_view, name='track_mood'),
    path('mood-tracker/', views.mood_tracker, name='mood_tracker'),    # Add this line
    path('assessment/', views.assessment_view, name='assessment'),
    path('book-appointment/', views.book_appointment, name='book_appointment'),
    path('journal/', views.journal_view, name='journal'),
    path('resources/', views.resources_view, name='resources'),
    path('wellness-plan/', views.wellness_plan_view, name='wellness_plan'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/update/', views.update_profile, name='update_profile'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('meditation/', views.meditation_view, name='meditation'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
