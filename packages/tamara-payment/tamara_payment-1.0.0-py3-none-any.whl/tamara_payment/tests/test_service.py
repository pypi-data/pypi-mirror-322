from decimal import Decimal
import json

from unittest.mock import Mock
from django.http import Http404
from django.conf import settings
from django.test import SimpleTestCase
from django.test import override_settings
from django.test.client import RequestFactory
from mock.mock import patch
from rest_framework import status

from tamara_payment.tests.mixins import MockResponseMixin

try:
    settings.configure()
except RuntimeError:
    pass


@override_settings(
    HASH_SECRET_KEY="test-hash-secret-key",
    PZ_SERVICE_CLASS="tamara_payment.commerce.dummy.Service",
)
class TestCheckoutService(SimpleTestCase, MockResponseMixin):
    def setUp(self):
        from tamara_payment.commerce.checkout import CheckoutService

        self.service = CheckoutService()
        self.request_factory = RequestFactory()

    @patch("tamara_payment.commerce.dummy.Service.get")
    @patch("tamara_payment.commerce.checkout.CheckoutService.generate_hash")
    @patch("tamara_payment.commerce.checkout.CheckoutService.generate_salt")
    def test_get_data(self, mock_generate_salt, mock_generate_hash, mock_get):
        mock_generate_hash.return_value = "test-hash"
        mock_generate_salt.return_value = "test-salt"
        mocked_response = self._mock_response(
            status_code=200,
            content=self._get_response("orders_checkout_response"),
            headers={"Content-Type": "application/json"},
        )
        mock_get.return_value = mocked_response

        request = self.request_factory.get("/payment-gateway/tamara/")
        basket_data = self.service.get_data(request)
        basket_data = json.loads(basket_data)

        self.assertEqual(basket_data["salt"], "test-salt")
        self.assertEqual(basket_data["hash"], "test-hash")

        self.assertEqual(basket_data["tax_amount"], {"amount": "37.92"})
        self.assertEqual(basket_data["shipping_amount"], {"amount": "33.00"})

        basket_items = [
            {
                "name": "Petıt / 110x170cm Dijital Baskılı Halı",
                "type": "Halı",
                "reference_id": 923,
                "sku": "2672881033026",
                "quantity": 4,
                "total_amount": {
                    "amount": "224.76"
                }
            },
            {
                "name": "50cm Bombeli Saat Desen 13",
                "type": "Duvar Saatleri",
                "reference_id": 922,
                "sku": "2672880349036",
                "quantity": 2,
                "total_amount": {
                    "amount": "79.84"
                }
            },
            {
                "name": "Demet Lavanta Çiçek 62cm",
                "type": "Yapay Çiçek",
                "reference_id": 921,
                "sku": "2672881041106",
                "quantity": 3,
                "total_amount": {
                    "amount": "30.96"
                }
            }
        ]
        self.assertEqual(basket_data["order_items"],  basket_items)

    @patch("tamara_payment.commerce.dummy.Service.get")
    def test_retrieve_pre_oder(self, mock_get):
        mocked_response = self._mock_response(
            status_code=200,
            content=self._get_response("orders_checkout_response"),
            headers={"Content-Type": "application/json"},
        )
        mock_get.return_value = mocked_response

        request = self.request_factory.get("/payment-gateway/tamara/")
        response = self.service._retrieve_pre_order(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("pre_order", response.data)

    @patch("tamara_payment.commerce.dummy.Service.get")
    def test_get_basket_items(self, mock_get):
        mocked_response = self._mock_response(
            status_code=200,
            content=self._get_response("orders_checkout_response"),
            headers={"Content-Type": "application/json"},
        )
        mock_get.return_value = mocked_response

        request = self.request_factory.get("/payment-gateway/tamara/")
        shipping_amount, tax_total_amount, basket_items = self.service._get_order_data(request)
        self.assertEqual(tax_total_amount, "37.92")
        self.assertEqual(shipping_amount, "33.00")

        expected_basket_item = [
            {
                "name": "Petıt / 110x170cm Dijital Baskılı Halı",
                "type": "Halı",
                "reference_id": 923,
                "sku": "2672881033026",
                "quantity": 4,
                "total_amount": {
                    "amount": "224.76"
                }
            },
            {
                "name": "50cm Bombeli Saat Desen 13",
                "type": "Duvar Saatleri",
                "reference_id": 922,
                "sku": "2672880349036",
                "quantity": 2,
                "total_amount": {
                    "amount": "79.84"
                }
            },
            {
                "name": "Demet Lavanta Çiçek 62cm",
                "type": "Yapay Çiçek",
                "reference_id": 921,
                "sku": "2672881041106",
                "quantity": 3,
                "total_amount": {
                    "amount": "30.96"
                }
            }
        ]
        self.assertEqual(
            basket_items, expected_basket_item
        )

    @patch("hashlib.sha512")
    @patch("tamara_payment.commerce.checkout.conf.HASH_SECRET_KEY", new="test-hash-secret-key")
    def test_get_hash(self, mock_sha512):
        session_id = "test-session-id"
        self.service.generate_hash(session_id, "test-salt")
        mock_sha512.assert_called_once_with(
            "test-salt|test-session-id|test-hash-secret-key".encode("utf-8")
        )

    @patch("secrets.token_hex")
    def test_generate_salt(self, mock_token_hex):
        self.service.generate_salt()
        mock_token_hex.assert_called_once()
        
    def test_get_product_name(self):
        product_name = None
        self.assertEqual(self.service._get_product_name(product_name), "none")
        
        product_name = "t" * 254
        self.assertEqual(self.service._get_product_name(product_name), product_name)
             
        product_name = "t" * 255
        self.assertEqual(self.service._get_product_name(product_name), product_name)
        
        product_name = "t" * 256
        self.assertEqual(self.service._get_product_name(product_name), "t" * 255)
        
    def test__find_decimal_places(self):
        self.assertEqual(self.service._find_decimal_places("10.000"), 3)
        self.assertEqual(self.service._find_decimal_places("10.00"), 2)
        self.assertEqual(self.service._find_decimal_places("10.0"), 1)
        self.assertEqual(self.service._find_decimal_places("10"), 0)
        
    def test__get_quantize_format(self):
        self.assertEqual(self.service._get_quantize_format("10.000"), Decimal(".001"))
        self.assertEqual(self.service._get_quantize_format("10.00"), Decimal(".01"))
        self.assertEqual(self.service._get_quantize_format("10.0"), Decimal(".1"))
        self.assertEqual(self.service._get_quantize_format("10"), Decimal("0"))
    
    def test__validate_checkout_step(self):
        mock_resp = Mock()
        mock_resp.data = {}
        
        with self.assertRaises(Http404):
            self.service._validate_checkout_step(mock_resp)
        
        mock_resp.data = {"pre_order": {"shipping_option": None}}
        with self.assertRaises(Http404):
            self.service._validate_checkout_step(mock_resp)

        mock_resp.data = {
            "context_list": [{"page_name": "ShippingOptionSelectionPage"}],
            "pre_order": {
                "shipping_option": {
                    "pk": 2,
                    "name": "Yurtici Kargo",
                    "slug": "yurtici",
                    "logo": None,
                    "shipping_amount": "9.99",
                    "description": None,
                    "kwargs": {}
                        }
                }
        }
        with self.assertRaises(Http404):
            self.service._validate_checkout_step(mock_resp)
            
        mock_resp.data = {
            "context_list": [{"page_name": "PaymentOptionSelectionPage"}],
            "pre_order": {
                "shipping_option": {
                    "pk": 2,
                    "name": "Yurtici Kargo",
                    "slug": "yurtici",
                    "logo": None,
                    "shipping_amount": "9.99",
                    "description": None,
                    "kwargs": {}
                },
                 "unpaid_amount": 10,
            },
        }
        self.service._validate_checkout_step(mock_resp)
