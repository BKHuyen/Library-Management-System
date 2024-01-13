from datetime import datetime
from random import random
from secrets import choice
from sys import prefix
from unicodedata import category
from django import forms
from numpy import require
from lmsApp import models
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm, UserChangeForm
from django.contrib.auth.models import User
import datetime


class SaveUser(forms.ModelForm):
    first_name = forms.CharField(max_length=250, help_text="The First name field is required.")
    middle_name = forms.CharField(max_length=250, required= False)
    last_name = forms.CharField(max_length=250, help_text="The Last name field is required.")
    username = forms.CharField(max_length=250,help_text="The Username field is required.")
    birth_date = forms.DateField(required= False)
    gender = forms.CharField(max_length=250, required= False)
    contact = forms.CharField(max_length=250, required= False)
    email = forms.CharField(max_length=250, help_text="The Email field is required.")
    address = forms.Textarea()
    is_active = forms.CharField(max_length=2)
    password1 =  forms.CharField(
        label=("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    

    class Meta:
        model = models.CustomUser
        fields = ('first_name', 'middle_name', 'last_name', 'username', 'birth_date', 'gender', 'contact', 'email', 'address', 'is_active', 'password1', )
    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            user = models.CustomUser.objects.exclude(id=self.cleaned_data['id']).get(email = email)
        except Exception as e:
            return email
        raise forms.ValidationError(f"This email is already exists/taken")

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            user = models.CustomUser.objects.exclude(id=self.cleaned_data['id']).get(username = username)
        except Exception as e:
            return username
        raise forms.ValidationError(f"This username is already exists/taken")
class UpdateProfile(UserChangeForm):
    username = forms.CharField(max_length=250,help_text="The Username field is required.")
    email = forms.EmailField(max_length=250,help_text="The Email field is required.")
    first_name = forms.CharField(max_length=250,help_text="The First Name field is required.")
    middle_name = forms.CharField(max_length=250, required=False)
    last_name = forms.CharField(max_length=250,help_text="The Last Name field is required.")
    #current_password = forms.CharField(max_length=250)
    birth_date = forms.DateField(required=False)
    gender = forms.CharField(max_length=250, required=False)
    contact = forms.CharField(max_length=250, required=False)
    address = forms.Textarea()
    
    class Meta:
        model = models.CustomUser
        fields = ('email', 'username','first_name', 'middle_name', 'last_name', 'birth_date', 'gender', 'contact', 'address')
    """
    def clean_current_password(self):
        if not self.instance.check_password(self.cleaned_data['current_password']):
            raise forms.ValidationError(f"Password is Incorrect")
    """
    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            user = User.objects.exclude(id=self.cleaned_data['id']).get(email = email)
        except Exception as e:
            return email
        raise forms.ValidationError(f"The {user.email} mail is already exists/taken")

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            user = User.objects.exclude(id=self.cleaned_data['id']).get(username = username)
        except Exception as e:
            return username
        raise forms.ValidationError(f"The {user.username} mail is already exists/taken")

class UpdateUser(UserChangeForm):
    first_name = forms.CharField(max_length=250, help_text="The First name field is required.")
    middle_name = forms.CharField(max_length=250, required= False)
    last_name = forms.CharField(max_length=250, help_text="The Last name field is required.")
    username = forms.CharField(max_length=250,help_text="The Username field is required.")
    birth_date = forms.DateField(required=False)
    gender = forms.CharField(max_length=250, required=False)
    contact = forms.CharField(max_length=250, required=False)
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
        raise forms.ValidationError(f"This email is already exists/taken")

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            user = models.CustomUser.objects.exclude(id=self.cleaned_data['id']).get(username = username)
        except Exception as e:
            return username
        raise forms.ValidationError(f"This username is already exists/taken")

class UpdatePasswords(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control form-control-sm rounded-0'}), label="Current Password")
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control form-control-sm rounded-0'}), label="New Password")
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control form-control-sm rounded-0'}), label="Confirm Password")
    class Meta:
        model = models.CustomUser
        fields = ('old_password','new_password1', 'new_password2')
    
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

class SaveBook(forms.ModelForm):
    category = forms.CharField(max_length=250)
    title = forms.CharField(max_length=250)
    description = forms.Textarea()
    publisher = forms.Textarea()
    date_published = forms.CharField(max_length=20)
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
    
    def clean_title(self):
        title = self.cleaned_data['title']
        try:
            book = models.Books.objects.exclude(id=self.cleaned_data['id']).get(title = title)
        except Exception as e:
            return title
        raise forms.ValidationError(f"This book is already exists/taken")

class SaveBorrow(forms.ModelForm):
    user = forms.CharField(max_length=250)
    book = forms.CharField(max_length=250)
    borrowing_date = forms.DateField()
    return_date = forms.DateField()
    quantity = forms.IntegerField()
    status = forms.CharField(max_length=2)

    class Meta:
        model = models.Borrow
        fields = ('user', 'book', 'borrowing_date', 'return_date', 'quantity', 'status', )

    def clean_user(self):
        user = int(self.data['user']) if (self.data['user']).isnumeric() else 0
        try:
            user = models.CustomUser.objects.get(id = user)
            return user
        except:
            raise forms.ValidationError("Invalid user.")       
    def clean_book(self):
        book = int(self.data['book']) if (self.data['book']).isnumeric() else 0
        try:
            book = models.Books.objects.get(id = book)
            return book
        except:
            raise forms.ValidationError("Invalid Book.")

