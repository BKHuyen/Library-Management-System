from distutils.command.upload import upload
from email.policy import default
from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image
from django.contrib.auth.models import User, AbstractBaseUser, AbstractUser
from django.contrib.auth.base_user import BaseUserManager



# Create your models here.
class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=250)
    description = models.TextField(blank=True, null= True)
    status = models.CharField(max_length=2, choices=(('1','Active'), ('2','Inactive')), default = 1)
    delete_flag = models.IntegerField(default = 0)
    date_added = models.DateTimeField(default = timezone.now)
    

    class Meta:
        verbose_name_plural = "List of Categories"

    def __str__(self):
        return str(f"{self.name}")
    
class CustomUser(AbstractUser):
    middle_name = models.CharField(max_length=150, blank=True, null= True)
    gender = models.CharField(max_length=20, choices=(('Nam','Nam'), ('Nữ','Nữ'), ('Khác', 'Khác')), default = 'Nam')
    contact = models.CharField(max_length=100)
    address = models.TextField(blank=True, null= True)
    birth_date = models.DateField(blank=True, null=True)
    #is_active = models.IntegerField(max_length=2, choices=(('1','Active'), ('2','Inactive')), default = 1)
    groups = models.ManyToManyField('auth.Group', related_name='customuser_groups', blank=True)
    user_permissions = models.ManyToManyField('auth.Permission', related_name='customuser_user_permissions', blank=True)
    


class Books(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.ForeignKey(Category, on_delete= models.CASCADE, related_name="category_id_fk")
    title = models.CharField(max_length=250)
    description = models.TextField(blank=True, null= True)
    author = models.TextField(blank=True, null= True)
    publisher = models.TextField(blank=True, null= True)
    date_published = models.CharField(max_length=20)
    quantity = models.IntegerField(default = 0)
    status = models.CharField(max_length=2, choices=(('1','Active'), ('2','Inactive')), default = 1)
    delete_flag = models.IntegerField(default = 0)
    date_added = models.DateTimeField(default = timezone.now)

    class Meta:
        verbose_name_plural = "List of Books"

    def __str__(self):
        return str(f"{self.id} - {self.title}")

class Borrow(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="user_id_fk")
    book = models.ForeignKey(Books, on_delete=models.CASCADE, related_name="book_id_fk")
    borrowing_date = models.DateField()
    return_date = models.DateField()
    quantity = models.IntegerField(default=0)
    status = models.CharField(max_length=2, choices=(('1', 'Pending'), ('2', 'Returned')), default=1)
    date_added = models.DateTimeField(default = timezone.now)
    class Meta:
        verbose_name_plural = "Borrowing Transactions"

    def __str__(self):
        return f"{self.user.id} - {self.book.id}"

class Post(models.Model):
    title = models.CharField(max_length=80)
    content = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title

