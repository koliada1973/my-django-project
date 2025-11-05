from django.db import models
from datetime import date
from decimal import Decimal
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# Модель Позичальника (Клієнта)
# Ми використовуємо стандартного користувача Django для аутентифікації клієнтів
from django.contrib.auth.models import User



# Створюємо об'єкт валідатора для ІПН
from django.core.validators import RegexValidator # Імпортуємо валідатор для регулярних виразів
# r'^\d{10}$' це регулярний вираз, який означає:
# ^ - початок рядка
# \d{10} - рівно 10 цифр
# $ - кінець рядка
numeric_validator = RegexValidator(
    r'^\d{10}$',
    'Введіть коректний ІПН. Поле має містити рівно 10 цифр, без літер та символів.'
)



class Client(models.Model):
    # User – це вбудована в Django модель, яка відповідає за аутентифікацію (вхід/вихід),
    # безпеку (хешування паролів) і базові ідентифікаційні дані (логін, ім'я, прізвище).
    # Зв'язок "Один до Одного" з користувачем Django - для того, щоб в подальшому клієнти могли входити на сайт під своїм логіном/паролем
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    # Додаткові поля, яких немає в джанго-моделі User:
    middle_name = models.CharField(max_length=100, verbose_name="По-батькові")
    IPN = models.CharField(
        max_length=10,
        verbose_name="ІПН",
        validators=[numeric_validator]  # Застосовуємо наш валідатор
    )
    phone_number = models.CharField(max_length=20, verbose_name="Номер телефону")
    address = models.CharField(max_length=255, verbose_name="Адреса")
    date_of_birth = models.DateField(verbose_name="Дата народження", null=True, blank=True)

    @property
    def full_name(self):
        return f"{self.user.last_name} {self.user.first_name} {self.middle_name}"

    def __str__(self):
        return self.full_name

    # class Meta:
    #     verbose_name = "Клієнт"
    #     verbose_name_plural = "Клієнти"


class Credit(models.Model):
    client = models.ForeignKey('Client', on_delete=models.CASCADE,related_name='credits', verbose_name="Клієнт")

    summa_credit = models.DecimalField(max_digits=10, decimal_places=2,verbose_name="Основна сума кредиту")
    percent = models.DecimalField(max_digits=5, decimal_places=3,verbose_name="Добова відсоткова ставка (%)")
    start_date = models.DateField(verbose_name="Дата видачі")
    srok_months = models.IntegerField(verbose_name="Термін кредиту (місяці)")
    day_of_pay = models.IntegerField(
        verbose_name="Плановий день оплати",
        help_text="День місяця (від 1 до 28), коли має бути платіж.",
        default=15,
        validators=[MinValueValidator(1), MaxValueValidator(28)]
    )

    def __str__(self):
        return f"Кредит №{self.id} на суму {self.summa_credit} UAH ({self.percent}% на день) для {self.client}"

    # class Meta:
    #     verbose_name = "Кредит"
    #     verbose_name_plural = "Кредити"




class Payment(models.Model):
    # Зв'язок "Багато до Одного": Багато платежів до одного кредиту
    credit = models.ForeignKey('Credit', on_delete=models.CASCADE,related_name='payments', verbose_name="Кредит")

    pay = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Сума платежу")
    date_pay = models.DateField(default=date.today, verbose_name="Дата платежу")

    def __str__(self):
        return f"Платіж {self.pay} UAH по кредиту №{self.credit.id} від {self.date_pay}"

    # class Meta:
    #     verbose_name = "Платіж"
    #     verbose_name_plural = "Платежі"
    #     ordering = ['-date_pay']
