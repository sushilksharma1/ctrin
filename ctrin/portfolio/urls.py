from django.urls import path
from .views import (
    HomeView, ProjectListView, ProjectDetailView,
    ServiceListView, TeamView, BlogListView, BlogDetailView,
    ContactView
)

app_name = 'portfolio'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('projects/', ProjectListView.as_view(), name='projects'),
    path('projects/<slug:slug>/', ProjectDetailView.as_view(), name='project_detail'),
    path('services/', ServiceListView.as_view(), name='services'),
    path('team/', TeamView.as_view(), name='team'),
    path('blog/', BlogListView.as_view(), name='blog'),
    path('blog/<slug:slug>/', BlogDetailView.as_view(), name='blog_detail'),
    path('contact/', ContactView.as_view(), name='contact'),
]
