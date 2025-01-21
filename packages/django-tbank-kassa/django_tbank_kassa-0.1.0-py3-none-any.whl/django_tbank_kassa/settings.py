from django.conf import settings

TBANK_KASSA_TERMINAL_KEY = getattr(settings, 'TBANK_KASSA_TERMINAL_KEY', None)

TBANK_KASSA_PASSWORD = getattr(settings, 'TBANK_KASSA_PASSWORD', None)

TBANK_KASSA_TEST = getattr(settings, 'TBANK_KASSA_TEST', None)

