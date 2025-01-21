from django.db import models


class Payment(models.Model):
    class Status(models.TextChoices):
        NEW = 'NEW', 'Новая сессия'
        FORM_SHOWED = 'FORM_SHOWED', 'Показ формы привязки карты'
        THREEDS_CHECKING = '3DS_CHECKING', 'Отправка клиента на проверку 3DS'
        THREEDS_CHECKED = '3DS_CHECKED', 'Клиент успешно прошел проверку 3DS'
        AUTHORIZING = 'AUTHORIZING', 'Отправка платежа на 0 руб'
        AUTHORIZED = 'AUTHORIZED', 'Платеж на 0 руб прошел успешно'
        COMPLETED = 'COMPLETED', 'Привязка успешно завершена'
        REJECTED = 'REJECTED', 'Привязка отклонена'

    id = models.CharField(
        verbose_name='ID заказа в системе мерчанта',
        max_length=36,
        primary_key=True,
        unique=True,
    )
    created_at = models.DateTimeField(
        verbose_name='Создан в',
        auto_now_add=True,
        editable=False,
    )
    amount = models.DecimalField(
        verbose_name='Сумма',
        max_digits=15,
        decimal_places=2,
    )
    status = models.CharField(
        verbose_name='Статус',
        max_length=20,
        choices=Status.choices,
    )
    payment_id = models.CharField(
        verbose_name='ID платежа в системе Т‑Кассы',
        max_length=20,
    )
    payment_url = models.URLField(
        verbose_name='Ссылка для оплаты',
    )

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'
