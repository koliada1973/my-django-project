from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Client, Credit, Payment



class ClientAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'IPN', 'phone_number', 'address')
    fields = ('user', 'middle_name', 'IPN', 'phone_number', 'address', 'date_of_birth')
    readonly_fields = ('full_name',)
    search_fields = ('user__username', 'phone_number')

    def has_module_permission(self, request):
        # Заборонити показ цього розділу у меню
        return request.user.is_superuser

    def get_full_name(self, obj):
        return f"{obj.user.last_name} {obj.user.first_name}"

    get_full_name.short_description = "Повне ім'я клієнта"

admin.site.register(Client, ClientAdmin)


class CreditAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'summa_credit', 'percent', 'start_date', 'srok_months')
    search_fields = ('client__user__username', 'id')

admin.site.register(Credit, CreditAdmin)


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('credit', 'pay', 'date_pay')

admin.site.register(Payment, PaymentAdmin)


class ClientInlineForUser(admin.StackedInline):
    model = Client
    can_delete = False
    verbose_name_plural = 'Деталі Клієнта'
    fields = ('middle_name', 'IPN', 'phone_number', 'address', 'date_of_birth',)
    readonly_fields = ('full_name',)

admin.site.unregister(User)

@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    inlines = (ClientInlineForUser,)
    list_display = ('username', 'email','last_name', 'first_name', 'is_active')

    # Обмеження видимості секцій
    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)

        # Якщо користувач не суперюзер — приховуємо блок "Permissions"
        if not request.user.is_superuser:
            filtered = []
            for name, section in fieldsets:
                if name != 'Permissions':
                    filtered.append((name, section))
            return filtered
        return fieldsets

    # Поля лише для читання (менеджер не може міняти статуси)
    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser:
            return ('is_staff', 'is_superuser', 'user_permissions', 'groups')
        return super().get_readonly_fields(request, obj)

    # Обмеження видимих користувачів
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        # Менеджер бачить тільки клієнтів (не staff)
        return qs.filter(is_staff=False, is_superuser=False)

    # Коли менеджер створює користувача — він завжди клієнт
    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            obj.is_staff = False
            obj.is_superuser = False
        super().save_model(request, obj, form, change)
