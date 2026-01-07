from django.urls import path
from chatbot_app import views  # Replace 'chatbot_app' with your actual app name

urlpatterns = [
    path('signup/', views.faculty_signup, name='faculty_signup'),
    path('login/', views.faculty_login, name='faculty_login'),
    path('logout/', views.faculty_logout, name='faculty_logout'),
    path('chatbot/', views.chatbot_page, name='chatbot_page'),
    path('get_response/', views.get_response, name='get_response'),
    path('', views.chatbot_page, name='home'),  # New root path
]