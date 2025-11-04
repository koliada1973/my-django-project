from django.contrib import admin

from .models import Client, Credit, Payment
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin


class ClientAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'phone_number', 'address')
    search_fields = ('user__username', 'phone_number')  # Пошук за логіном та телефоном

admin.site.register(Client, ClientAdmin)

class CreditAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'summa_credit', 'percent', 'start_date', 'srok_months')
    search_fields = ('client__user__username', 'id')

admin.site.register(Credit, CreditAdmin)


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('credit', 'pay', 'date_pay')

admin.site.register(Payment, PaymentAdmin)


# 2.1 Вбудована форма для додавання деталей Клієнта на сторінку User
class ClientInlineForUser(admin.StackedInline):
    model = Client
    can_delete = False
    verbose_name_plural = 'Деталі Клієнта'
    fields = ('phone_number', 'address', 'date_of_birth',)


# 2.2 Перевизначаємо форму User для вбудовування Client та керування правами
admin.site.unregister(User)  # Видаляємо стандартний User


@admin.register(User)
class CustomUserAdmin(AuthUserAdmin):
    inlines = (ClientInlineForUser,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')

    def save_model(self, request, obj, form, change):
        if not change:
            obj.is_staff = False
        super().save_model(request, obj, form, change)
