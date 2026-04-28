from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('category/<int:category_id>/', views.ad_by_category, name='advens_by_category'),
    path('advens/<int:ad_id>/', views.ad, name='advens'),
    path('advens/add/', views.add_advens, name='add_advesn'),
    path('category/add/', views.add_category, name='add_category'),
    path('category/<int:category_id>/update/', views.update_category, name='update_cateogory'),
    path('advens/<int:advens_id>/update/', views.update_advens, name='update_advens'),
    path('category/<int:category_id>/delete/', views.delete_category, name='delete_category'),
    path('advens/<int:advens_id>/delete/', views.delete_advens, name='delete_advens'),
    path('advens/<int:adversiment_id>/comment/', views.create_comment, name='create_comment'),
    path('advens/<int:comment_id>/comment/update', views.update_comment, name='update_comment'),
    path('advens/<int:comment_id>/<int:advens_id>/comment/delete/', views.delete_comment, name='delete_comment')
]