# django_tbank_kassa

django_tbank_kassa is a Django library for integrating with Tinkoff Bank's payment system. It simplifies the process of managing payments by providing tools to handle payments and webhooks with minimal setup.

## Features

- Easy integration with Tinkoff Bank's API.
- Handles payment creation and status updates.
- Provides built-in views and serializers for payments.
- Configurable via environment variables.

## Installation

1. Install the package using pip:
   ```bash
   pip install django_tbank_kassa
   ```

2. Add `django_tbank_kassa` to your `INSTALLED_APPS` in the Django settings file:
   ```python
   INSTALLED_APPS = [
       # ... other apps ...
       'django_tbank_kassa',
   ]
   ```

3. Add the following settings to your Django project:
   ```python
   TBANK_KASSA_TERMINAL_KEY = 'your_terminal_key'
   TBANK_KASSA_PASSWORD = 'your_password'
   TBANK_KASSA_TEST = True  # Set to False for production
   ```

## Usage

### Configuration

Ensure the following settings are configured in your Django project:

- `TBANK_KASSA_TERMINAL_KEY`: Your Tinkoff Bank terminal key.
- `TBANK_KASSA_PASSWORD`: Your Tinkoff Bank password.
- `TBANK_KASSA_TEST`: Set to `True` for testing mode or `False` for production.

### Payment Model

django_tbank_kassa provides a `Payment` model. Migrations will create the necessary database tables for storing payment details.

Run the migrations:
```bash
python manage.py migrate
```

### Views

The library includes views for handling payment creation and retrieving payment details. Add the following to your `urls.py`:

```python
from django.urls import path
from django_tbank_kassa.generics import ListCreatePaymentView, RetrievePaymentView, TBankWebhookView

urlpatterns = [
    path('payments/', ListCreatePaymentView.as_view(), name='list_create_payment'),
    path('payments/<str:id>/', RetrievePaymentView.as_view(), name='retrieve_payment'),
    path('webhook/', TBankWebhookView.as_view(), name='webhook'),
]
```

### Creating Payments

To create a new payment, send a POST request to the `/payments/` endpoint with the following data:

- `id` (string): A unique identifier for the payment.
- `amount` (decimal): The amount of the payment.

Example:
```json
{
  "id": "order123",
  "amount": "1000.00"
}
```
The response will include the payment status, a payment ID, and a URL to complete the payment.

### Handling Webhooks

Tinkoff Bank sends webhook events to notify about payment status changes. Configure the webhook URL (e.g., `/webhook/`) in your Tinkoff Bank account settings.

When a webhook is received, the library validates it and updates the corresponding payment status. You can customize the webhook handling by extending the `TBankWebhookView` and overriding its methods if necessary.

## Example Project

Here is an example of integrating django_tbank_kassa into a Django project:

1. Add the app and configure the settings as described above.
2. Add the provided URLs to your `urls.py`.
3. Use the `/payments/` endpoint to create and manage payments.
4. Register the webhook URL with Tinkoff Bank.
