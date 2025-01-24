import logging

from django.http import Http404
from django.views.generic import View
from django.template.response import TemplateResponse

from tamara_payment.commerce.checkout import CheckoutService
from tamara_payment.forms import TamaraForm
from tamara_payment.commerce import conf


logger = logging.getLogger(__name__)


class TamaraPaymentView(View):
    checkout_service = CheckoutService()

    def get(self, request):
        if not conf.TAMARA_EXTENSION_URL:
            logging.exception("Missing TAMARA_EXTENSION_URL")            
            raise Http404
        
        data = self.checkout_service.get_data(request)
        session_id = request.GET.get("sessionId")
  
        tamara_form = TamaraForm(
            initial={"data": data}
        )

        return TemplateResponse(
            request=request,
            template="tamara_payment.html",
            context={
                "action_url": f"{conf.TAMARA_EXTENSION_URL}/form-page?sessionId={session_id}",
                "action_method": "POST",
                "tamara_form": tamara_form,
            },
        )
