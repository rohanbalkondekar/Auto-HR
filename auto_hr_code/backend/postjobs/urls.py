from django.urls import path
from . import views

urlpatterns = [
    path('get_jobs/', views.get_jobs, name='get_jobs'),
    path('post_job_preview/', views.post_job_preview, name='post_job'),
    path('post_jobs/', views.post_job, name='post_job'),
    path('get_suggestions/', views.get_suggestions, name='get_suggestions'),
    path('post_application/', views.post_application, name='post_application'),
    path('get_application/<str:application_id>/', views.get_application, name='get_applications_for_job'),
    path('get_applications_for_job/<str:job_id>/', views.get_applications_for_job, name='get_applications_for_job'),
    path('delete_job/<str:job_id>/', views.delete_job, name='delete_job'),
    path('edit_job/<str:job_id>/', views.edit_job, name='edit_job'),
    path('get_all_applications/', views.get_all_applications, name='get_all_applications'),
    path('get_top_applications/', views.get_top_applications, name='get_top_applications'),
    path('send_emails/', views.send_emails, name='send_emails'),
    path('interview/<str:application_id>/', views.interview, name='interview'),
    path('evaluate_interview/<str:application_id>/', views.evaluate_interview, name='interview'),
    path('get_all_interviews/', views.get_all_interviews, name='get_all_interviews'),
    path('get_interviews_for_job/<str:job_id>/', views.get_interviews_for_job, name='get_all_interviews'),
]