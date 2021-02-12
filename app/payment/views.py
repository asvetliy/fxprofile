from django.views import View
from django.views.defaults import page_not_found
from .models import PaymentSystem
from django.contrib.auth.mixins import LoginRequiredMixin


class PaymentURLDispatcher(LoginRequiredMixin, View):
    @staticmethod
    def _get_scheme_class(kls):
        schemes_module = __import__('payment.schemes')
        if hasattr(schemes_module.schemes, kls):
            return getattr(schemes_module.schemes, kls)
        else:
            return None

    def post(self, request, payment, action):
        payment_system = PaymentSystem.objects.get(code=payment)
        if payment_system and payment_system.is_enabled:
            scheme_class = self._get_scheme_class(payment_system.cls)
            p = scheme_class()
            if action == 'init':
                return p.init_payment(request)
            if action == 'process':
                return p.process_payment(request)
        return page_not_found(request, None)

    def get(self, request, payment, action):
        payment_system = PaymentSystem.objects.get(code=payment)
        if payment_system and payment_system.is_enabled:
            scheme_class = self._get_scheme_class(payment_system.cls)
            if scheme_class is None:
                return page_not_found(request, None)
            p = scheme_class()
            if action == 'success':
                return p.success_payment(request)
            if action == 'fail':
                return p.fail_payment(request)
        return page_not_found(request, None)
