import datetime
from django.shortcuts import redirect, render
import json
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse
from lmsApp import models, forms
from django.db.models import Q, Count, Sum
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from .models import Post  # New
from django.http import JsonResponse
from django.views import View

def product_search(request):
    return render(request, 'index.html')

class ProductAutocomplete(View):
    def get(self, request):
        query = request.GET.get('term', '')
        books = models.Books.objects.filter(name__icontains=query)[:10]
        results = [book.title for book in books]
        return JsonResponse(results, safe=False)

def context_data(request):
    fullpath = request.get_full_path()
    abs_uri = request.build_absolute_uri()
    abs_uri = abs_uri.split(fullpath)[0]
    context = {
        'system_host' : abs_uri,
        'page_name' : '',
        'page_title' : '',
        'system_name' : 'Library Managament System',
        'topbar' : True,
        'footer' : True,
    }

    return context
    
def userregister(request):
    context = context_data(request)
    context['topbar'] = False
    context['footer'] = False
    context['page_title'] = "User Registration"
    if request.user.is_authenticated:
        return redirect("home-page")
    return render(request, 'register.html', context)

def save_register(request):
    resp={'status':'failed', 'msg':''}
    if not request.method == 'POST':
        resp['msg'] = "No data has been sent on this request"
    else:
        form = forms.SaveUser(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your Account has been created succesfully")
            resp['status'] = 'success'
        else:
            for field in form:
                for error in field.errors:
                    if resp['msg'] != '':
                        resp['msg'] += str('<br />')
                    resp['msg'] += str(f"[{field.name}] {error}.")
            
    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def update_profile(request):
    context = context_data(request)
    context['page_title'] = 'Update Profile'
    user = models.CustomUser.objects.get(id = request.user.id)
    print(request.method)
    if not request.method == 'POST':
        form = forms.UpdateProfile(instance=user)
        context['form'] = form
        
    else:
        form = forms.UpdateProfile(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile has been updated")
            return redirect("profile-page")
        else:
            context['form'] = form
            
    return render(request, 'manage_profile.html',context)

@login_required
def update_password(request):
    context =context_data(request)
    context['page_title'] = "Update Password"
    user = models.CustomUser.objects.get(id = request.user.id)
    if request.method == 'POST':
        form = forms.UpdatePasswords(user = request.user, data= request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Your Account Password has been updated successfully")
            update_session_auth_hash(request, form.user)
            return redirect("profile-page")
        else:
            context['form'] = form
    else:
        form = forms.UpdatePasswords(request.POST)
        context['form'] = form
    return render(request,'update_password.html',context)

# Create your views here.
def login_page(request):
    context = context_data(request)
    context['topbar'] = True
    context['footer'] = False
    context['page_name'] = 'login'
    context['page_title'] = 'Login'
    return render(request, 'login.html', context)

def login_user(request):
    logout(request)
    resp = {"status":'failed','msg':''}
    username = ''
    password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                resp['status']='success'
            else:
                resp['msg'] = "Incorrect username or password"
        else:
            resp['msg'] = "Incorrect username or password"
    return HttpResponse(json.dumps(resp),content_type='application/json')

@login_required
def home(request):
    context = context_data(request)
    context['page'] = 'home'
    context['page_title'] = 'Home'
    context['categories'] = models.Category.objects.filter(delete_flag = 0, status = 1).all().count()
    context['books'] = models.Books.objects.filter(delete_flag = 0, status = 1).all().count()
    context['pending'] = models.Borrow.objects.filter(status = 1).all().count()
    context['pending'] = models.Borrow.objects.filter(status = 1).all().count()
    context['transactions'] = models.Borrow.objects.all().count()

    return render(request, 'home.html', context)

def logout_user(request):
    logout(request)
    return redirect('login-page')
    
@login_required
def profile(request):
    context = context_data(request)
    context['page'] = 'profile'
    context['page_title'] = "Profile"
    return render(request,'profile.html', context)

@login_required
def users(request):
    context = context_data(request)
    context['page'] = 'users'
    context['page_title'] = "User List"
    context['users'] = models.CustomUser.objects.exclude(pk=request.user.pk).filter(is_superuser = False).all()
    return render(request, 'users.html', context)

@login_required
def save_user(request):
    resp = { 'status': 'failed', 'msg' : '' }
    if request.method == 'POST':
        post = request.POST
        if not post['id'] == '':
            user = models.CustomUser.objects.get(id = post['id'])
            form = forms.UpdateUser(request.POST, instance=user)
        else:
            form = forms.SaveUser(request.POST) 

        if form.is_valid():
            form.save()
            if post['id'] == '':
                messages.success(request, "User has been saved successfully.")
            else:
                messages.success(request, "User has been updated successfully.")
            resp['status'] = 'success'
        else:
            for field in form:
                if field.field.required and not field.value():
                    for error in field.errors:
                        if not resp['msg'] == '':
                            resp['msg'] += str('<br/>')
                        resp['msg'] += str(f'[{field.name}] {error}')
    else:
         resp['msg'] = "There's no data sent on the request"

    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def view_user(request, pk = None):
    context = context_data(request)
    context['page'] = 'view_user'
    context['page_title'] = 'View User'
    if pk is None:
        context['user'] = {}
    else:
        context['user'] = models.CustomUser.objects.get(id=pk)
    
    return render(request, 'view_user.html', context)

@login_required
def manage_user(request, pk = None):
    context = context_data(request)
    context['page'] = 'manage_user'
    context['page_title'] = 'Manage User'
    if pk is None:
        context['user'] = {}
    else:
        context['user'] = models.CustomUser.objects.get(id=pk)
    
    return render(request, 'manage_user.html', context)

@login_required
def delete_user(request, pk = None):
    resp = { 'status' : 'failed', 'msg':''}
    if pk is None:
        resp['msg'] = 'User ID is invalid'
    else:
        try:
            models.CustomUser.objects.filter(pk = pk).delete()
            messages.success(request, "User has been deleted successfully.")
            resp['status'] = 'success'
        except:
            resp['msg'] = "Deleting User Failed"

    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def category(request):
    context = context_data(request)
    context['page'] = 'category'
    context['page_title'] = "Category List"
    context['category'] = models.Category.objects.filter(delete_flag = 0).all()
    return render(request, 'category.html', context)

@login_required
def save_category(request):
    resp = { 'status': 'failed', 'msg' : '' }
    if request.method == 'POST':
        post = request.POST
        if not post['id'] == '':
            category = models.Category.objects.get(id = post['id'])
            form = forms.SaveCategory(request.POST, instance=category)
        else:
            form = forms.SaveCategory(request.POST) 

        if form.is_valid():
            form.save()
            if post['id'] == '':
                messages.success(request, "Category has been saved successfully.")
            else:
                messages.success(request, "Category has been updated successfully.")
            resp['status'] = 'success'
        else:
            for field in form:
                for error in field.errors:
                    if not resp['msg'] == '':
                        resp['msg'] += str('<br/>')
                    resp['msg'] += str(f'[{field.name}] {error}')
    else:
         resp['msg'] = "There's no data sent on the request"

    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def view_category(request, pk = None):
    context = context_data(request)
    context['page'] = 'view_category'
    context['page_title'] = 'View Category'
    if pk is None:
        context['category'] = {}
    else:
        context['category'] = models.Category.objects.get(id=pk)
    
    return render(request, 'view_category.html', context)

@login_required
def manage_category(request, pk = None):
    context = context_data(request)
    context['page'] = 'manage_category'
    context['page_title'] = 'Manage Category'
    if pk is None:
        context['category'] = {}
    else:
        context['category'] = models.Category.objects.get(id=pk)
    
    return render(request, 'manage_category.html', context)

@login_required
def delete_category(request, pk = None):
    resp = { 'status' : 'failed', 'msg':''}
    if pk is None:
        resp['msg'] = 'Category ID is invalid'
    else:
        try:
            models.Category.objects.filter(pk = pk).update(delete_flag = 1)
            messages.success(request, "Category has been deleted successfully.")
            resp['status'] = 'success'
        except:
            resp['msg'] = "Deleting Category Failed"

    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def books(request):
    context = context_data(request)
    context['page'] = 'book'
    context['page_title'] = "Book List"
    context['books'] = models.Books.objects.filter(delete_flag = 0).all()
    return render(request, 'books.html', context)

@login_required
def save_book(request):
    resp = { 'status': 'failed', 'msg' : '' }
    if request.method == 'POST':
        post = request.POST
        
        if not post['id'] == '':
            book = models.Books.objects.get(id = post['id'])
            form = forms.SaveBook(request.POST,instance = book)
        else:

            form = forms.SaveBook(request.POST) 

        if form.is_valid():
            form.save()
            if post['id'] == '':
                messages.success(request, "Book has been saved successfully.")
            else:
                messages.success(request, "Book has been updated successfully.")
            resp['status'] = 'success'
        else:
            for field in form:
                for error in field.errors:
                    if not resp['msg'] == '':
                        resp['msg'] += str('<br/>')
                    resp['msg'] += str(f'[{field.name}] {error}')
    else:
         resp['msg'] = "There's no data sent on the request"

    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def view_book(request, pk = None):
    context = context_data(request)
    context['page'] = 'view_book'
    context['page_title'] = 'View Book'
    if pk is None:
        context['book'] = {}
    else:
        context['book'] = models.Books.objects.get(id=pk)
    
    return render(request, 'view_book.html', context)

@login_required
def manage_book(request, pk = None):
    context = context_data(request)
    context['page'] = 'manage_book'
    context['page_title'] = 'Manage Book'
    if pk is None:
        context['book'] = {}
    else:
        context['book'] = models.Books.objects.get(id=pk)
    context['categories'] = models.Category.objects.filter(delete_flag = 0, status = 1).all()
    return render(request, 'manage_book.html', context)

@login_required
def delete_book(request, pk = None):
    resp = { 'status' : 'failed', 'msg':''}
    if pk is None:
        resp['msg'] = 'Book ID is invalid'
    else:
        try:
            models.Books.objects.filter(pk = pk).update(delete_flag = 1)
            messages.success(request, "Book has been deleted successfully.")
            resp['status'] = 'success'
        except:
            resp['msg'] = "Deleting Book Failed"

    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def borrows(request):
    context = context_data(request)
    context['page'] = 'borrow'
    context['page_title'] = "Borrowing Transaction List"
    
    context['borrows'] = models.Borrow.objects.order_by('user__username').all()
    
    return render(request, 'borrows.html', context)

@login_required
def user_borrows(request):
    context = context_data(request)
    context['page'] = 'user_borrow'
    context['page_title'] = "Borrowing Transaction List"
    
    context['user_borrows'] = models.Borrow.objects.filter(user=request.user).all()
    
    return render(request, 'user_borrow.html', context)

@login_required
def save_borrow(request):
    resp = { 'status': 'failed', 'msg' : '' }
    if request.method == 'POST':
        post = request.POST
        user = request.POST.get('user')
        print(user)
        if not post['id'] == '':
            borrow = models.Borrow.objects.get(id = post['id'])
            form = forms.SaveBorrow(request.POST, instance=borrow)
            if form.is_valid():
                
                form.save()
                if post['id'] == '':
                    messages.success(request, "Borrowing Transaction has been saved successfully.")
                else:
                    messages.success(request, "Borrowing Transaction has been updated successfully.")
                resp['status'] = 'success'
            else:
                for field in form:
                    for error in field.errors:
                        if not resp['msg'] == '':
                            resp['msg'] += str('<br/>')
                        resp['msg'] += str(f'[{field.name}] {error}')
        else:
            form = forms.SaveBorrow(request.POST) 
            if form.is_valid():
                total_books_borrowed = models.Borrow.objects.filter(user__id=user, status='1').aggregate(total=Sum('quantity'))
                print(total_books_borrowed)
                if total_books_borrowed['total'] >=3:
                    
                    resp['msg'] = "The user have borrowed the maximum allowed number of books."
                else:
                    form.save()
                    if post['id'] == '':
                        messages.success(request, "Borrowing Transaction has been saved successfully.")
                    else:
                        messages.success(request, "Borrowing Transaction has been updated successfully.")
                    resp['status'] = 'success'
            else:
                for field in form:
                    for error in field.errors:
                        if not resp['msg'] == '':
                            resp['msg'] += str('<br/>')
                        resp['msg'] += str(f'[{field.name}] {error}')
            
    else:
         resp['msg'] = "There's no data sent on the request"

    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def view_borrow(request, pk = None):
    context = context_data(request)
    context['page'] = 'view_borrow'
    context['page_title'] = 'View Transaction Details'
    if pk is None:
        context['borrow'] = {}
    else:
        context['borrow'] = models.Borrow.objects.get(id=pk)
    
    return render(request, 'view_borrow.html', context)

@login_required
def manage_borrow(request, pk = None):
    context = context_data(request)
    context['page'] = 'manage_borrow'
    context['page_title'] = 'Manage Transaction Details'
    if pk is None:
        context['borrow'] = {}
    else:
        context['borrow'] = models.Borrow.objects.get(id=pk)
    context['users'] = models.CustomUser.objects.filter(is_active = True, is_superuser = 0).all()
    context['books'] = models.Books.objects.filter(delete_flag = 0, status = 1).all()
    return render(request, 'manage_borrow.html', context)

@login_required
def delete_borrow(request, pk = None):
    resp = { 'status' : 'failed', 'msg':''}
    if pk is None:
        resp['msg'] = 'Transaction ID is invalid'
    else:
        try:
            models.Borrow.objects.filter(pk = pk).delete()
            messages.success(request, "Transaction has been deleted successfully.")
            resp['status'] = 'success'
        except:
            resp['msg'] = "Deleting Transaction Failed"

    return HttpResponse(json.dumps(resp), content_type="application/json")
