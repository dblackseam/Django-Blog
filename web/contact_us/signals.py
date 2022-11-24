from .models import Feedback
from django.db.models.signals import post_save, pre_save
# from django.core.signals import request_started
from django.dispatch import receiver
from .services import ContactUsService


# Способ подключения сигнала №2 - Идеальный вариант ✔
@receiver(post_save, sender=Feedback)  # Первым аргументом передаем тип сигнала, вторым (т.е. именованым sender)
# передаем ту модель ЭКЗЕМПЛЯРА КОТОРОЙ должны присылать сигналы.
# sender - Класс МОДЕЛИ с которыми будут работать сигналы.
def send_answer_to_user(instance: Feedback, created, **kwargs):
    # instance - Сам по себе экземпляр модели который мы будем менять (Create, Update or Delete). Т.е. именно тот
    # экземпляр от которого именно пришел сигнал.
    # created - Это очень полезный аргумент помогающий понять был ли объект СОЗДАН или ОБНОВЛЕН.
    # Подозреваю что если возвращается True то это значит что произошло именно создание объекта. А если False -
    # обновление.
    if created:
        return

    if instance.status == Feedback.Status.PROCESSED:
        return

    if instance.answer:
        instance.status = Feedback.Status.PROCESSED
        instance.save(update_fields=["status"])
        service = ContactUsService(instance)
        service.send_answer_to_user()

# Способ подключения сигнала №1
# post_save.connect(send_answer_to_user, sender=Feedback)
