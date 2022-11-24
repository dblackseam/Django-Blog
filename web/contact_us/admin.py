from django.contrib import admin

from .models import Feedback
from .services import ContactUsService


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'status')
    # list_editable = ('status',) # добавляет возможность изменять поле в странице со всеми записями. (при этом
    # запись будет изменяться сразу же, без необходимости сделать save к примеру, как в карточке самой записи.
    search_fields = ("email",)

    # Способ №1 - с Save
    # def save_model(self, request, obj, form, change):
    #     super().save_model(request, obj, form, change)
    #     if obj.status == "Processed":
    #         return
    #     if obj.answer:
    #         obj.status = "Processed"
    #         obj.save()
    #         service = ContactUsService(obj)
    #         service.send_answer_to_user()

