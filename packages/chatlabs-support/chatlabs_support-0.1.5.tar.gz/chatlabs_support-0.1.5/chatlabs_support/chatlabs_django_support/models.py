from django.apps import apps
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models


class TelegramUser(models.Model):
    telegram_id = models.BigIntegerField(
        primary_key=True,
        unique=True,
    )

    class Meta:
        swappable = 'SUPPORT_TELEGRAM_USER_MODEL'
        abstract = True

    @classmethod
    def get_model(cls) -> type['TelegramUser']:
        return apps.get_model(settings.SUPPORT_TELEGRAM_USER_MODEL)


class Ticket(models.Model):
    id = models.BigAutoField(
        verbose_name='ID',
        primary_key=True,
        unique=True,
    )
    created_at = models.DateTimeField(
        verbose_name='Создан в',
        auto_now_add=True,
    )
    user: models.ForeignKey[TelegramUser] = models.ForeignKey(
        verbose_name='Пользователь',
        to=settings.SUPPORT_TELEGRAM_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tickets',
    )
    title = models.CharField(
        verbose_name='Заголовок',
        max_length=256,
    )
    support_manager = models.ForeignKey(
        verbose_name='Менеджер поддержки',
        to=User,
        on_delete=models.SET_NULL,
        related_name='tickets',
        null=True,
        blank=True,
    )
    resolved = models.BooleanField(
        verbose_name='Решен',
        default=False,
    )

    class Meta:
        verbose_name = 'Тикет'
        verbose_name_plural = 'Тикеты'

    def __str__(self):
        return self.title


class Message(models.Model):
    class Sender(models.TextChoices):
        USER = 'user', 'Пользователь'
        SUPPORT_MANAGER = 'supp', 'Менеджер поддержки'

    id = models.BigAutoField(
        verbose_name='ID',
        primary_key=True,
        unique=True,
    )
    created_at = models.DateTimeField(
        verbose_name='Создано в',
        auto_now_add=True,
    )
    ticket = models.ForeignKey(
        verbose_name='Тикет',
        to=Ticket,
        on_delete=models.CASCADE,
        related_name='messages',
    )
    sender = models.CharField(
        verbose_name='Отправитель',
        max_length=4,
        choices=Sender.choices,
        default=Sender.USER,
    )
    text = models.CharField(
        verbose_name='Текст',
        max_length=4096,
    )
    viewed = models.BooleanField(
        verbose_name='Просмотрено',
        default=False,
    )

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

    def __str__(self):
        text = f'{self.text[:20]}...'
        sender = self.sender_instance
        if sender is None:
            return text
        return f'{sender}: {text}'

    @property
    def sender_instance(self) -> TelegramUser | User | None:
        match self.sender:
            case self.Sender.USER:
                return self.ticket.user
            case self.Sender.SUPPORT_MANAGER:
                return self.ticket.support_manager
            case _:
                return None
