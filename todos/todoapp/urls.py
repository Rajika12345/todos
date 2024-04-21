from django.urls import path
from todoapp import views

urlpatterns=[
    path("todo/add/",views.TodoCreateView.as_view(),name="todo-add"),
    path("todo/all/",views.TodoListView.as_view(),name="todo-list"),
    path("todo/<int:pk>/change/",views.TodoUpdateView.as_view(),name="todo-edit"),
    path("todo/<int:pk>/remove/",views.TodoDeleteView.as_view(),name="todo-delete"),
    path("todo/<int:pk>/",views.TodoDetailView.as_view(),name="todo-detail"),
    path("register/",views.SignupView.as_view(),name="signup"),
    path("",views.SigninView.as_view(),name="signin"),
    path("signout/",views.SignOutView.as_view(),name="signout"),
]

