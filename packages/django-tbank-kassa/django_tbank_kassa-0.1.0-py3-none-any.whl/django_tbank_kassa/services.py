from typing import Unpack

from tbank_kassa import TBankAPI
from tbank_kassa.enums import TBankKassaEnvironment
from tbank_kassa.models.dicts import InitDict

from django_tbank_kassa import models, settings

tbank_api = TBankAPI(
    terminal_key=settings.TBANK_KASSA_TERMINAL_KEY,
    password=settings.TBANK_KASSA_PASSWORD,
    environment=(
        TBankKassaEnvironment.TEST
        if settings.TBANK_KASSA_TEST
        else TBankKassaEnvironment.PROD
    ),
)


def init_payment(**kwargs: Unpack[InitDict]) -> models.Payment:
    payment = tbank_api.init_payment(**kwargs)
    return models.Payment.objects.create(
        id=payment.order_id,
        amount=payment.amount,
        status=payment.status,
        payment_id=payment.payment_id,
        payment_url=payment.payment_url,
    )
