from django.db import models
from django.utils.translation import gettext_lazy as _


class Feedback(models.Model):
    class Status(models.TextChoices):
        UNPROCESSED = ("Unprocessed", "Unprocessed")
        PROCESSED = ("Processed", "Processed")

    name = models.CharField(max_length=100)
    email = models.EmailField()
    content = models.TextField()
    image = models.ImageField(null=True, upload_to="contact_us/")
    status = models.CharField(choices=Status.choices, default="Unprocessed", max_length=300)
    answer = models.TextField(blank=True)  # Использовать null в textfield нельзя! Потому что пустые текстовые
    # значения и так будут пустыми. null=True, это про базу данных. blank=True это про валидацию, в форме к примеру
    # можно будет оставить это поле пустым.

    class Meta:
        verbose_name = _('Feedback')
