from django.conf.urls import url

from tamara_payment.views import TamaraPaymentView

urlpatterns = [
    url(r"^$", TamaraPaymentView.as_view(), name="tamara-payment"),
]
