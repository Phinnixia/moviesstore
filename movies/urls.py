from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='movies.index'),
    path('<int:id>/', views.show, name='movies.show'),
    path('<int:id>/review/create/', views.create_review, name='movies.create_review'),
    path('<int:id>/review/<int:review_id>/edit/',views.edit_review, name='movies.edit_review'),
    path('<int:id>/review/<int:review_id>/delete/', views.delete_review, name='movies.delete_review'),
    #UPVOTE
    path('<int:id>/review/<int:review_id>/upvote/', views.increment_upvote, name='movies.increment_upvote'),
    path('comments/', views.comments, name='movies.comments'),
    #PETITIONS
    path('petitions/', views.petitions, name='movies.petitions'),
    path('petitions/create/', views.create_petition, name='movies.create_petition'),
    path('<int:id>/vote', views.vote, name='movies.vote'),
]