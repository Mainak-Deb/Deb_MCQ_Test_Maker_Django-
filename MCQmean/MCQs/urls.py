from django.contrib import admin
from django.urls import path
from MCQs import views

urlpatterns = [
    path('', views.home,name='home'),
    path('home/', views.home,name='home'),
    path("signup/", views.handleSignup, name="handleSignup"),
	path("login/", views.handleLogin, name="handleLogin"),
	path("logout/", views.handleLogout, name="handleLogout"),
    path("create/", views.createform, name="createform"),
    path("examset/", views.questionset, name="questionset"),
    path("addqs/", views.addqs, name="addqs"),
    path("added/", views.qsadded, name="qsadded"),
    path("dashboard/<str:name>/", views.dashboard, name="dashboard"),
    path("edit/", views.edit, name="edit"),
    path("preview/", views.preview, name="preview"),
    path("test/<str:examid>/", views.test, name="test"),
    path("evaluate/", views.evaluate, name="evaluate"),
    path("marks/", views.marks, name="marks"),

]
