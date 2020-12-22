from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"), 
    path("create", views.create, name="create"),
    path("auctions/<int:id>.html", views.listing, name="listing"),
    path("addcomment/<int:id>", views.addcomment, name="addcomment"), 
    path("addwatchlist/<int:id>", views.addwatchlist, name="addwatchlist"), 
    path("watchlist", views.watchlist, name="watchlist"), 
    path("removewatchlist/<int:id>", views.removewatchlist, name="removewatchlist"),
    path("bid/<int:id>", views.bid, name="bid"), 
    path("close/<int:id>", views.close, name="close"), 
    path("closed", views.closed, name="closed"), 
    path("categories", views.categories, name="categories"), 
    path("categorypage/<str:title>", views.categorypage, name="categorypage")
]
