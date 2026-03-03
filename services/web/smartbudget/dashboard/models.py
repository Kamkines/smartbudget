from django.db import models

class User(models.Model): #Наследуем от базового класса
    telegram_id = models.BigIntegerField(unique=True)
    username = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta: # настройка модели
        db_table = "users"
        managed = False  # Django не управляет этой таблицей, она уже в БД и чисто все данные берутся из БД
        

    def __str__(self): # отображать объект в виде строки 
        return self.username


class Category(models.Model):
    name = models.CharField(max_length=100)
    emoji = models.CharField(max_length=10)
    is_default = models.BooleanField(default=False)

    class Meta:
        db_table = "categories"
        managed = False

    def __str__(self):
        return f"{self.emoji} {self.name}"


class Transaction(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=500)
    created_at = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column="user_id")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, db_column="category_id")

    class Meta:
        db_table = "transactions"
        managed = False

    def __str__(self):
        return f"{self.amount} - {self.description}"