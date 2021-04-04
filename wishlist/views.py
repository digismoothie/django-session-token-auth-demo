import shopify
from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.signals import user_logged_in
from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic
from pyactiveresource.connection import UnauthorizedAccess
from shopify_auth.session_tokens.views import get_scope_permission


class SplashPageView(generic.View):
    template_name = "wishlist/splashpage.html"

    def get(self, request):
        myshopify_domain = request.GET.get("shop")

        if not myshopify_domain:
            return HttpResponse("Shop parameter missing.")
        try:
            shop = get_user_model().objects.get(myshopify_domain=myshopify_domain)
        except get_user_model().DoesNotExist:
            return get_scope_permission(request, myshopify_domain)

        with shop.session:
            try:
                shopify_shop = shopify.Shop.current()
            except UnauthorizedAccess:
                shop.uninstall()
                return get_scope_permission(request, myshopify_domain)

        user_logged_in.send(sender=shop.__class__, request=request, user=shop)

        return render(
            request,
            self.template_name,
            {
                "data": {
                    "shopOrigin": shop.myshopify_domain,
                    "apiKey": getattr(settings, "SHOPIFY_APP_API_KEY"),
                    "loadPath": request.GET.get(REDIRECT_FIELD_NAME) or "/home",
                }
            },
        )


class ShopifyLoginRequiredMixin(LoginRequiredMixin):
    def get_login_url(self):
        shop = self.request.GET.get("shop")
        if shop:
            return settings.LOGIN_URL + f"?shop={shop}"
        return settings.LOGIN_URL


class HomeView(ShopifyLoginRequiredMixin, generic.TemplateView):
    template_name = "wishlist/index.html"

    def get(self, request):

        with request.user.session:
            try:
                shopify_shop = shopify.Shop.current()
                message = shopify_shop.email
            except UnauthorizedAccess as e:
                message = str(e)
        return self.render_to_response({"title": message})


class ProductsView(ShopifyLoginRequiredMixin, generic.TemplateView):
    template_name = "wishlist/index.html"

    def get(self, request):
        with request.user.session:
            products = shopify.Product.find(limit=10)
        return self.render_to_response({"products": products})
