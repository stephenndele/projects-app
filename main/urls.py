from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    path('', views.home, name='home'),
    path('details/<int:id>', views.details, name='details'),
    path('addprojects', views.add_projects, name='add_projects'),
    path('editprojects/<int:id>/', views.edit_projects, name='edit_projects'),
    path('deleteprojects/<int:id>/', views.delete_projects, name='delete_projects'),
    path('addreviews/<int:id>/', views.add_review, name='add_review'),
    path('editreview/<int:project_id>/<int:review_id>/', views.edit_review, name='edit_review'),
    path('deletereview/<int:project_id>/<int:review_id>/', views.delete_review, name='delete_review'),
    path("user/", views.userpage, name = "userpage"),
    path('api/project/', views.ProjectList.as_view()),

]