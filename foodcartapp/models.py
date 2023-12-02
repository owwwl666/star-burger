from django.db import models
from django.core.validators import MinValueValidator
from phonenumber_field.modelfields import PhoneNumberField
from django.db.models import F, Sum
from django.utils import timezone


class Restaurant(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )
    address = models.CharField(
        'адрес',
        max_length=100,
        blank=True,
    )
    contact_phone = models.CharField(
        'контактный телефон',
        max_length=50,
        blank=True,
    )

    class Meta:
        verbose_name = 'ресторан'
        verbose_name_plural = 'рестораны'

    def __str__(self):
        return self.name


class ProductQuerySet(models.QuerySet):
    def available(self):
        products = (
            RestaurantMenuItem.objects
            .filter(availability=True)
            .values_list('product')
        )
        return self.filter(pk__in=products)


class OrderQuerySet(models.QuerySet):
    def calculate_final_price(self):
        return self.select_related('restaurant').annotate(
            final_price=Sum(F('ordered_products__order_price'))
        )


class ProductCategory(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )
    category = models.ForeignKey(
        ProductCategory,
        verbose_name='категория',
        related_name='products',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    price = models.DecimalField(
        'цена',
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    image = models.ImageField(
        'картинка'
    )
    special_status = models.BooleanField(
        'спец.предложение',
        default=False,
        db_index=True,
    )
    description = models.TextField(
        'описание',
        max_length=200,
        blank=True,
    )

    objects = ProductQuerySet.as_manager()

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'

    def __str__(self):
        return self.name


class RestaurantMenuItem(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        related_name='menu_items',
        verbose_name="ресторан",
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='menu_items',
        verbose_name='продукт',
    )
    availability = models.BooleanField(
        'в продаже',
        default=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'пункт меню ресторана'
        verbose_name_plural = 'пункты меню ресторана'
        unique_together = [
            ['restaurant', 'product']
        ]

    def __str__(self):
        return f"{self.restaurant.name} - {self.product.name}"


class Order(models.Model):
    RAW = 'raw'
    ASSEMBLY = 'assembly'
    COURIER = 'courier'
    DELIVER = 'delivered'

    CASH = 'cash'
    NON_CASH = 'non-cash'

    ORDER_STATUS = [
        (RAW, 'Необработанный'),
        (ASSEMBLY, 'Сборка'),
        (COURIER, 'Передан курьеру'),
        (DELIVER, 'Доставлен')
    ]

    PAYMENT_METHOD = [
        (CASH, 'Наличностью'),
        (NON_CASH, 'Электронно'),
    ]

    firstname = models.CharField(
        max_length=200,
        verbose_name='Имя заказчика'
    )
    lastname = models.CharField(
        max_length=200,
        verbose_name='Фамилия заказчика'
    )
    phonenumber = PhoneNumberField(
        region='RU',
        verbose_name='Номер телефона',
        db_index=True
    )
    address = models.CharField(
        max_length=200,
        verbose_name='Адрес доставки'
    )

    registrated_at = models.DateTimeField(
        default=timezone.now(),
        verbose_name='Дата создания заказа',
        db_index=True
    )

    called_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='Дата звонка менеджера',
        db_index=True
    )

    delivered_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='Дата доставки',
        db_index=True
    )

    status = models.CharField(
        max_length=30,
        choices=ORDER_STATUS,
        default=RAW,
        verbose_name='Статус заказа',
        db_index=True
    )

    payment = models.CharField(
        max_length=30,
        null=True,
        blank=True,
        choices=PAYMENT_METHOD,
        default=CASH,
        verbose_name='Способ оплаты',
        db_index=True
    )

    comment = models.TextField(
        blank=True,
        verbose_name='Комментарий'
    )

    restaurant = models.ForeignKey(
        'Restaurant',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='Исполнитель заказа'
    )

    objects = OrderQuerySet.as_manager()

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f"{self.firstname} {self.lastname} {self.address}"


class ProductOrder(models.Model):
    order = models.ForeignKey(
        'Order',
        on_delete=models.CASCADE,
        related_name='ordered_products',
        verbose_name='Заказ'
    )
    product = models.ForeignKey(
        'Product',
        on_delete=models.CASCADE,
        related_name='ordered_products',
        verbose_name='Товар'
    )
    quantity = models.PositiveIntegerField(
        verbose_name='Количество',
        db_index=True
    )

    order_price = models.DecimalField(
        'Цена заказа',
        max_digits=8,
        decimal_places=2,
        db_index=True,
        validators=[MinValueValidator(0)],
        default=0
    )

    class Meta:
        verbose_name = 'Товар в заказе'
        verbose_name_plural = 'Товары в заказе'

    def __str__(self):
        return f"{self.product.name}"
