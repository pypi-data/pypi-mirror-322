import secrets
import hashlib
import json
import logging
from decimal import Decimal, ROUND_DOWN

from tamara_payment.commerce import conf

from django.conf import settings
from django.http import Http404
from importlib import import_module


module, _class = settings.PZ_SERVICE_CLASS.rsplit(".", 1)
Service = getattr(import_module(module), _class)

logger = logging.getLogger(__name__)


class CheckoutService(Service):
    def get_data(self, request):
        salt = self.generate_salt()
        session_id = request.GET.get("sessionId")
        
        hash_ = self.generate_hash(session_id, salt)
        shipping_amount, tax_total_amount, basket_items = self._get_order_data(request)

        return json.dumps({
            "hash": hash_,
            "salt": salt,
            "tax_amount": {"amount": tax_total_amount},
            "shipping_amount": {"amount": shipping_amount},
            "order_items": basket_items,
        }, ensure_ascii=False)

    def generate_salt(self):
        salt = secrets.token_hex(10)
        return salt

    def generate_hash(self, session_id, salt):
        hash_key = conf.HASH_SECRET_KEY
        return hashlib.sha512(
            f"{salt}|{session_id}|{hash_key}".encode("utf-8")
        ).hexdigest()

    def _get_product_name(self, product_name):
        if not product_name:
            product_name = "none"
        return product_name if len(product_name) <= 255 else product_name[:255]
  
    def _validate_checkout_step(self, response):
        if "pre_order" not in response.data:
            raise Http404()
        
        if response.data["pre_order"].get("shipping_option") is None:
            raise Http404()
        
        page_names = [page["page_name"] for page in response.data["context_list"]]
        if "PaymentOptionSelectionPage" not in page_names:
            raise Http404()
    
    def _find_decimal_places(self, price):
        if '.' in price:
            return len(price.split('.')[1])
        return 0
    
    def _get_quantize_format(self, price_as_string):
        decimal_places = self._find_decimal_places(price_as_string)
        if decimal_places == 0:
            return Decimal(0)
        quantize_format = Decimal(f".{'0' * (decimal_places-1)}1")
        return quantize_format
    
    def _get_order_data(self, request):
        response = self._retrieve_pre_order(request)
        self._validate_checkout_step(response=response)
        unpaid_amount = Decimal(response.data["pre_order"].get("unpaid_amount", 0))

        if unpaid_amount == Decimal(0):
            logger.info("Tamara Payment Unpaid amount is Zero")
            return []

        shipping_amount = Decimal(response.data["pre_order"]["shipping_amount"])
        shipping_amount = shipping_amount if shipping_amount < unpaid_amount else 0

        response_basket_items = response.data["pre_order"]["basket"]["basketitem_set"]
        quantize_format = self._get_quantize_format(response.data["pre_order"]["unpaid_amount"])
        total_product_amount = Decimal(response.data["pre_order"]["basket"]["total_product_amount"])
        unpaid_amount_without_shipping = unpaid_amount - shipping_amount
        remaining_amount = max(unpaid_amount_without_shipping - total_product_amount, 0)

        basket_items = []
        cumulative_amount = Decimal(0)
        total_tax_amount = Decimal(0)

        for index, item in enumerate(response_basket_items):
            basket_item_amount = Decimal(item["total_amount"])
            weight = basket_item_amount / total_product_amount
            amount = (remaining_amount * weight + basket_item_amount).quantize(quantize_format,
                                                                               ROUND_DOWN)
            cumulative_amount += amount

            if index == len(response_basket_items) - 1:
                # Adjust the amount for the last item to ensure the total matches unpaid amount
                delta = unpaid_amount_without_shipping - cumulative_amount
                amount = amount + delta

            tax_rate = Decimal(item.get("tax_rate", 0)) / 100

            total_tax_amount += (amount * tax_rate).quantize(quantize_format, ROUND_DOWN)
            basket_items.append({
                "name": self._get_product_name(item.get("product", {}).get("name")),
                "type": item.get("product", {}).get("category", {}).get("name"),
                "reference_id": item.get("pk"),
                "sku": item.get("product", {}).get("sku"),
                "quantity": item.get("quantity"),
                "total_amount": {
                    "amount": str(amount),
                }
            })

        return str(shipping_amount), str(total_tax_amount), basket_items

    def _retrieve_pre_order(self, request):
        path = "/orders/checkout/"
        response = self.get(
            path, request=request, headers={"X-Requested-With": "XMLHttpRequest"}
        )
        return self.normalize_response(response)
