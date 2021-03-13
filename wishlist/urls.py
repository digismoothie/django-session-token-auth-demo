from django.urls import path

import wishlist.views as views

app_name = "wishlist"

urlpatterns = [
    path("", views.SplashPageView.as_view(), name="dashboard"),
    path("home", views.HomeView.as_view(), name="home"),
    path("products", views.ProductsView.as_view(), name="products"),
    path("analytics", views.ProductsView.as_view(), name="analytics"),
]
