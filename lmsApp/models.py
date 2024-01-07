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
    

"""
class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete= models.CASCADE)
    name = models.CharField(max_length=250)
    description = models.TextField(blank=True, null= True)
    status = models.CharField(max_length=2, choices=(('1','Active'), ('2','Inactive')), default = 1)
    delete_flag = models.IntegerField(default = 0)
    date_added = models.DateTimeField(default = timezone.now)
    date_created = models.DateTimeField(auto_now = True)

    class Meta:
        verbose_name_plural = "List of Categories"

    def __str__(self):
        return str(f"{self.category} - {self.name}")
"""
class Books(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.ForeignKey(Category, on_delete= models.CASCADE, related_name="category_id_fk")
    title = models.CharField(max_length=250)
    description = models.TextField(blank=True, null= True)
    author = models.TextField(blank=True, null= True)
    publisher = models.TextField(blank=True, null= True)
    date_published = models.DateTimeField()
    quantity = models.IntegerField(default = 0)
    status = models.CharField(max_length=2, choices=(('1','Active'), ('2','Inactive')), default = 1)
    delete_flag = models.IntegerField(default = 0)
    date_added = models.DateTimeField(default = timezone.now)

    class Meta:
        verbose_name_plural = "List of Books"

    def __str__(self):
        return str(f"{self.ID} - {self.title}")

"""
class Member(models.Model):
    ID = models.IntegerField()
    first_name = models.CharField(max_length=250)
    middle_name = models.CharField(max_length=250, blank=True, null= True)
    last_name = models.CharField(max_length=250)
    username = models.CharField(max_length=250)
    password = models.CharField(max_length=250)
    birth_date = models.DateTimeField()
    gender = models.CharField(max_length=20, choices=(('Nam','Nam'), ('Nữ','Nữ'), ('Khác', 'Khác')), default = 'Nam')
    contact = models.CharField(max_length=250)
    email = models.CharField(max_length=250)
    address = models.TextField(blank=True, null= True)
    status = models.CharField(max_length=2, choices=(('1','Active'), ('2','Inactive')), default = 1)
    delete_flag = models.IntegerField(default = 0)
    date_added = models.DateTimeField(default = timezone.now)

    class Meta:
        verbose_name_plural = "List of Members"

    def __str__(self):
        return str(f"{self.id} - {self.first_name}{' '+self.middle_name if not self.middle_name == '' else ''} {self.last_name}")

    def name(self):
        return str(f"{self.first_name}{' '+self.middle_name if not self.middle_name == '' else ''} {self.last_name}")
"""
class Borrow(models.Model):
    member = models.ForeignKey(CustomUser, on_delete= models.CASCADE, related_name="user_id_fk")
    borrowing_date = models.DateField()
    status = models.CharField(max_length=2, choices=(('1','Pending'), ('2','Returned')), default = 1)
    quantity = models.IntegerField(default = 0)
    class Meta:
        verbose_name_plural = "Borrowing Transactions"

    def __str__(self):
        return str(f"{self.member.id}")
    
class Borrow_detail(models.Model):
    book = models.ForeignKey(Books, on_delete= models.CASCADE, related_name="book_id_fk")
    borrow = models.ForeignKey(Borrow, on_delete= models.CASCADE, related_name="borrow_id_fk")
    return_date = models.DateField()
    class Meta:
        verbose_name_plural = "Borrowing Transactions"

    def __str__(self):
        return str(f"{self.book.id}")

class Post(models.Model):
    title = models.CharField(max_length=80)
    content = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title