from datetime import datetime
from random import random
from secrets import choice
from sys import prefix
from unicodedata import category
from django import forms
from numpy import require
from lmsApp import models

from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm, UserChangeForm
from django.contrib.auth.models import User
import datetime


class SaveUser(UserCreationForm):
    ID = forms.IntegerField()
    first_name = forms.CharField(max_length=250, help_text="The First name field is required.")
    middle_name = forms.CharField(max_length=250, required= False)
    last_name = forms.CharField(max_length=250, help_text="The Last name field is required.")
    username = forms.CharField(max_length=250,help_text="The Username field is required.")
    birth_date = forms.DateField()
    gender = forms.CharField(max_length=250)
    contact = forms.CharField(max_length=250)
    email = forms.CharField(max_length=250, help_text="The Email field is required.")
    address = forms.Textarea()
    is_active = forms.CharField(max_length=2)
    password1 = forms.CharField(max_length=250)
    password2 = forms.CharField(max_length=250)

    class Meta:
        model = models.CustomUser
        fields = ('ID', 'first_name', 'middle_name', 'last_name', 'username', 'birth_date', 'gender', 'contact', 'email', 'address', 'is_active', 'password1', 'password2',)

class UpdateProfile(forms.ModelForm):
    username = forms.CharField(max_length=250,help_text="The Username field is required.")
    email = forms.EmailField(max_length=250,help_text="The Email field is required.")
    first_name = forms.CharField(max_length=250,help_text="The First Name field is required.")
    middle_name = forms.CharField(max_length=250)
    last_name = forms.CharField(max_length=250,help_text="The Last Name field is required.")
    birth_date = forms.DateField()
    gender = forms.CharField(max_length=20)
    contact = forms.CharField(max_length=250)
    address = forms.Textarea()

    class Meta:
        model = models.CustomUser
        fields = ('email', 'username','first_name', 'middle_name', 'last_name', 'birth_date', 'gender', 'contact', 'address', )

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            user = models.CustomUser.objects.exclude(id=self.cleaned_data['id']).get(email = email)
        except Exception as e:
            return email
        raise forms.ValidationError(f"This mail is already exists/taken")

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            user = models.CustomUser.objects.exclude(id=self.cleaned_data['id']).get(username = username)
        except Exception as e:
            return username
        raise forms.ValidationError(f"The username is already exists/taken")

class UpdateUser(UserChangeForm):
    first_name = forms.CharField(max_length=250, help_text="The First name field is required.")
    middle_name = forms.CharField(max_length=250, required= False)
    last_name = forms.CharField(max_length=250, help_text="The Last name field is required.")
    username = forms.CharField(max_length=250,help_text="The Username field is required.")
    birth_date = forms.DateField()
    gender = forms.CharField(max_length=250)
    contact = forms.CharField(max_length=250)
    email = forms.CharField(max_length=250, help_text="The Email field is required.")
    address = forms.Textarea()
    
    class Meta:
        model = models.CustomUser
        fields = ('first_name', 'middle_name', 'last_name', 'username', 'birth_date', 'gender', 'contact', 'email', 'address',)

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            user = models.CustomUser.objects.exclude(id=self.cleaned_data['id']).get(email = email)
        except Exception as e:
            return email
        raise forms.ValidationError(f"This mail is already exists/taken")

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            user = models.CustomUser.objects.exclude(id=self.cleaned_data['id']).get(username = username)
        except Exception as e:
            return username
        raise forms.ValidationError(f"This username is already exists/taken")

class UpdatePasswords(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control form-control-sm rounded-0'}), label="Mật khẩu hiện tại")
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control form-control-sm rounded-0'}), label="Mật khẩu mới")
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control form-control-sm rounded-0'}), label="Xác nhận lại mật khẩu")
    class Meta:
        model = models.CustomUser
        fields = ('old_password','new_password1', 'new_password2')
    def clean_old_password(self):
        if not self.instance.check_password(self.cleaned_data['old_password']):
            raise forms.ValidationError(f"Password is Incorrect")

class SaveCategory(forms.ModelForm):
    name = forms.CharField(max_length=250)
    description = forms.Textarea()
    status = forms.CharField(max_length=2)

    class Meta:
        model = models.Category
        fields = ('name', 'description', 'status', )

    def clean_name(self):
        id = self.data['id'] if (self.data['id']).isnumeric() else 0
        name = self.cleaned_data['name']
        try:
            if id > 0:
                category = models.Category.objects.exclude(id = id).get(name = name, delete_flag = 0)
            else:
                category = models.Category.objects.get(name = name, delete_flag = 0)
        except:
            return name
        raise forms.ValidationError("Category Name already exists.")
"""
class SaveSubCategory(forms.ModelForm):
    category = forms.CharField(max_length=250)
    name = forms.CharField(max_length=250)
    description = forms.Textarea()
    status = forms.CharField(max_length=2)

    class Meta:
        model = models.SubCategory
        fields = ('category', 'name', 'description', 'status', )

    def clean_category(self):
        cid = int(self.data['category']) if (self.data['category']).isnumeric() else 0
        try:
            category = models.Category.objects.get(id = cid)
            return category
        except:
            raise forms.ValidationError("Invalid Category.")

    def clean_name(self):
        id = int(self.data['id']) if (self.data['id']).isnumeric() else 0
        cid = int(self.data['category']) if (self.data['category']).isnumeric() else 0
        name = self.cleaned_data['name']
        try:
            category = models.Category.objects.get(id = cid)
            if id > 0:
                sub_category = models.SubCategory.objects.exclude(id = id).get(name = name, delete_flag = 0, category = category)
            else:
                sub_category = models.SubCategory.objects.get(name = name, delete_flag = 0, category = category)
        except:
            return name
        raise forms.ValidationError("Sub-Category Name already exists on the selected Category.")
"""
class SaveBook(forms.ModelForm):
    category = forms.CharField(max_length=250)
    title = forms.CharField(max_length=250)
    description = forms.Textarea()
    publisher = forms.Textarea()
    date_published = forms.DateField()
    quantity = forms.IntegerField()
    status = forms.CharField(max_length=2)  
    author = forms.Textarea()
    
    class Meta:
        model = models.Books
        fields = ( 'category', 'title', 'description', 'publisher', 'date_published', 'quantity', 'status','author' )

    def clean_category(self):
        scid = int(self.data['category']) if (self.data['category']).isnumeric() else 0
        try:
            category = models.Category.objects.get(id = scid)
            return category
        except:
            raise forms.ValidationError("Invalid Category.")
    """
    def clean_isbn(self):
        id = int(self.data['id']) if (self.data['id']).isnumeric() else 0
        isbn = self.cleaned_data['isbn']
        try:
            if id > 0:
                book = models.Books.objects.exclude(id = id).get(isbn = isbn, delete_flag = 0)
            else:
                book = models.Books.objects.get(isbn = isbn, delete_flag = 0)
        except:
            return isbn
        raise forms.ValidationError("ISBN already exists on the Database.")"""
"""  
class SaveMember(forms.ModelForm):
    ID = forms.IntegerField()
    first_name = forms.CharField(max_length=250, help_text="The First name field is required.")
    middle_name = forms.CharField(max_length=250, required= False)
    last_name = forms.CharField(max_length=250, help_text="The Last name field is required.")
    username = forms.CharField(max_length=250,help_text="The Username field is required.")
    birth_date = forms.DateField()
    gender = forms.CharField(max_length=250)
    contact = forms.CharField(max_length=250)
    email = forms.CharField(max_length=250, help_text="The Email field is required.")
    address = forms.Textarea()
    status = forms.CharField(max_length=2)
    password = forms.CharField(max_length=250, help_text="The Password field is required.")
    

    class Meta:
        model = models.Member
        fields = ('first_name', 'middle_name', 'last_name', 'username', 'birth_date', 'gender', 'contact', 'email', 'address', 'status', 'password', )

    def clean_code(self):
        id = int(self.data['id']) if (self.data['id']).isnumeric() else 0
        code = self.cleaned_data['id']
        try:
            if id > 0:
                book = models.Member.objects.exclude(id = id).get(code = code, delete_flag = 0)
            else:
                book = models.Member.objects.get(code = code, delete_flag = 0)
        except:
            return code
        raise forms.ValidationError("Member Id already exists on the Database.")

class UpdateMember(UserChangeForm):
    first_name = forms.CharField(max_length=250,help_text="The First Name field is required.")
    middle_name = forms.CharField(max_length=250, required= False)
    last_name = forms.CharField(max_length=250,help_text="The Last Name field is required.")
    username = forms.CharField(max_length=250,help_text="The Username field is required.")
    gender = forms.CharField(max_length=250)
    contact = forms.CharField(max_length=250)
    email = forms.EmailField(max_length=250,help_text="The Email field is required.")
    address = forms.CharField(max_length=250)
    status = forms.CharField(max_length=2)
    password = forms.CharField(max_length=250, help_text="The Password field is required.")
    
    
    class Meta:
        model = models.Member
        fields = ('first_name', 'middle_name', 'last_name', 'username', 'gender', 'contact', 'email', 'address', 'status', 'password', )

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            user = models.Member.objects.exclude(id=self.cleaned_data['id']).get(email = email)
        except Exception as e:
            return email
        raise forms.ValidationError(f"The {user.email} mail is already exists/taken")

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            user = models.Member.objects.exclude(id=self.cleaned_data['id']).get(username = username)
        except Exception as e:
            return username
        raise forms.ValidationError(f"The {user.username} mail is already exists/taken")
"""
class SaveBorrow(forms.ModelForm):
    member = forms.CharField(max_length=250)
    book = forms.CharField(max_length=250)
    borrowing_date = forms.DateField()
    return_date = forms.DateField()
    status = forms.CharField(max_length=2)

    class Meta:
        model = models.Borrow
        fields = ('member', 'book', 'borrowing_date', 'return_date', 'status', )

    def clean_member(self):
        member = int(self.data['member']) if (self.data['member']).isnumeric() else 0
        try:
            member = models.Member.objects.get(id = member)
            return member
        except:
            raise forms.ValidationError("Invalid member.")
            
    def clean_book(self):
        book = int(self.data['book']) if (self.data['book']).isnumeric() else 0
        try:
            book = models.Books.objects.get(id = book)
            return book
        except:
            raise forms.ValidationError("Invalid Book.")
