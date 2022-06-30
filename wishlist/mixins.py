from __future__ import annotations

import logging

import shopify
from django.conf import settings
from django.contrib.auth.signals import user_logged_in
from django.shortcuts import redirect, render
from django.urls import reverse
from pyactiveresource.connection import UnauthorizedAccess
from shopify_auth.session_tokens import views as session_tokens_views

from wishlist.models import AuthAppShopUser


def create_charge(request, shop: AuthAppShopUser, shopify_shop: shopify.Shop, encoded_host: str):
    return_url = request.build_absolute_uri(
        reverse(settings.BILLING_REDIRECT_URL) + f"?shop={shop.myshopify_domain}&host={encoded_host}"
    )

    return shopify.RecurringApplicationCharge.create(
        {
            "name": "Example charge",
            "price": 9.99,
            "return_url": return_url,
            "trial_days": 14,
            "test": settings.SHOPIFY_APP_TEST_CHARGE,
        }
    )


class CreateChargeMixin:
    def should_charge(self, shopify_shop: shopify.Shop):
        """
        Charge only when shop is on paid plan.
        """
        return ((
                settings.SHOPIFY_APP_TEST_CHARGE
                or shopify_shop.plan_name not in ["partner_test", "affiliate", "staff_business", "trial"]
            )
            and not shopify.RecurringApplicationCharge.current()
        )

    def create_charge(self, request, shop: AuthAppShopUser, shopify_shop: shopify.Shop, encoded_host: str):
        charge = create_charge(request, shop, shopify_shop, encoded_host)
        return render(
            request,
            "shopify_auth/iframe_redirect.html",
            {
                "redirect_uri": charge.confirmation_url,
                "shop": shop.myshopify_domain,
            },
        )

