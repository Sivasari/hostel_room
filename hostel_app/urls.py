from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('book-room/', views.book_room, name='book_room'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('roommate-suggestions/', views.roommate_suggestions, name='roommate_suggestions'),
    path('verify-payments/', views.verify_payments, name='verify_payments'),
    path('submit-payment/', views.submit_payment, name='submit_payment'),

    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
]
