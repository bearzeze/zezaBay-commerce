from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    
    path("listings/<int:item_id>", views.listings, name="listings"),
    path("listings/create", views.create_listing, name="create"),
    path("listings/delete/<int:item_id>", views.delete_listing, name="delete_listing"),
    path("listings/edit/<int:item_id>", views.edit_listing, name="edit_listing"),
    path("listings/close/<int:item_id>", views.close_listing, name="close_listing"),
    
    
    path("categories/<int:category_id>", views.categories, name="categories"),
    
    path("user/listings/<str:username>", views.user_listings, name="user_listings"),
    path("user/watchlist/add/<int:item_id>", views.watchlist_add, name="watchlist_add"),
    path("user/watchlist/remove/<int:item_id>", views.watchlist_remove, name="watchlist_remove"),
    path("user/watchlist/", views.watchlist, name="watchlist"),
    
    path("comments/delete/<int:comment_id>", views.delete_comment, name="delete_comment"),
]
