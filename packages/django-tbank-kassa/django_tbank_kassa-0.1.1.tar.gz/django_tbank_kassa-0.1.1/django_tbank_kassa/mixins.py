from rest_framework.exceptions import AuthenticationFailed
from rest_framework.views import Request, Response

from django_tbank_kassa import models, services


class TBankWebhookMixin:
    def status_changed(
        self,
        request: Request,  # noqa: ARG002
        old_status: models.Payment.Status,  # noqa: ARG002
        new_status: models.Payment.Status,
    ):
        self.payment.status = new_status
        self.payment.save()

    def post(self, request: Request) -> Response:
        if not services.tbank_api.validate_webhook(request.data):
            raise AuthenticationFailed()
        try:
            self.payment = models.Payment.objects.get(
                id=request.data.get('OrderId')
            )
        except models.Payment.DoesNotExist:
            return Response('OK')
        if self.payment.status != (status := request.data.get('Status')):
            self.status_changed(
                request,
                models.Payment.Status(self.payment.status),
                models.Payment.Status(status),
            )
        return Response('OK')
