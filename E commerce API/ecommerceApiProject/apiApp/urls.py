from django.urls import path
from .views import *


urlpatterns=[
    path("product_list",product_list,name="product_list"),
    path("products/<slug:slug>",product_detail,name="product_detail"),
    path("category_list",category_list,name="category_list"),
    path("calegory/<slug:slug>",category_detail,name="category_detail"),
    path("add_to_cart/",add_to_cart,name="add_to_cart"),
    path("update_cartitem_quantity/",update_cartitem_quantity,name="update_cartitem_quantity"),
    path("add_review/",add_review,name="add_review"),
    path("update_review/<int:pk>/",update_review,name="update_review"),
    path("delete_review/<int:pk>/",delete_review,name="delete_review"),
    path("product_rating/<int:product_id>/", product_rating_view, name="product_rating"),
    path("add_rating/", add_rating, name="add_rating"),
    path('add_to_cart/',add_to_cart, name='add_to_cart'),
    path('delete_from_cart/',delete_from_cart, name='delete_from_cart'),
    

]