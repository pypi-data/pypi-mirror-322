from rest_framework.generics import ListCreateAPIView, RetrieveAPIView
from rest_framework.views import APIView

from django_tbank_kassa import mixins, models, serializers, services


class TBankWebhookView(mixins.TBankWebhookMixin, APIView):
    pass


class ListCreatePaymentView(ListCreateAPIView):
    queryset = models.Payment.objects.all()
    serializer_class = serializers.Payment

    def perform_create(self, serializer: serializer_class):
        payment = services.tbank_api.init_payment(
            order_id=serializer.validated_data.get('id'),
            amount=serializer.validated_data.get('amount'),
        )
        serializer.save(
            status=payment.status,
            payment_id=payment.payment_id,
            payment_url=payment.payment_url,
        )


class RetrievePaymentView(RetrieveAPIView):
    queryset = models.Payment.objects.all()
    serializer_class = serializers.Payment
    lookup_field = 'id'
