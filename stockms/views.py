import datetime
import sqlite3

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect

from customer.models import Customer
from product.models import Product

from purchase.models import Purchase
from stock.models import Stock
from .form import CustomerForm, ProductForm,  PurchaseForm, StockForm
# import xlwt

from django.http import HttpResponse
from django.contrib.auth.models import User


@login_required(login_url='login')
def index(request):
    return render(request, 'dashboard.html')


def signup(request):
    if request.method == 'GET':
        context = {
            'form': UserCreationForm(),
        }
        return render(request, 'signup.html', context)
    else:
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
        return render(request, 'signin.html', {'form': form})


def signin(request):
    if request.method == 'GET':
        context = {
            'form': AuthenticationForm()
        }
        return render(request, 'signin.html', context)
    else:
        u = request.POST.get('username')
        p = request.POST.get('password')
        user = authenticate(username=u, password=p)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return redirect('login')


def my_logout(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def customer(request):
    posts = []
    db = sqlite3.connect('db.sqlite3')
    cursor = db.cursor()
    cursor.execute(
        'select customer_customer.id, customer_customer.name , product_product.name , purchase_purchase.date , purchase_purchase.id from customer_customer , product_product , purchase_purchase where customer_customer.id=purchase_purchase.customer_id_id and product_product.id=purchase_purchase.product_id_id order by purchase_purchase.date desc')
    for obj in cursor.fetchall():
        posts.append({"id": obj[0], "name": obj[1], "product_id": obj[2], "date": obj[3], "purchase_id": obj[4]})
    if request.method == 'GET':
        context = {
            'form': CustomerForm(),
            'all_posts': posts,
            'year': getCurrentYear(),
        }
        return render(request, 'customer.html', context)
    else:
        form = CustomerForm(request.POST)
        if form.is_valid():
            mydata = form.save(commit=False)
            mydata.user_id = request.user.id
            mydata.save()
            return redirect('customer')
        return render(request, 'customer.html', {'form': form})


@login_required(login_url='login')
def product(request):
    if request.method == 'GET':
        context = {
            'form': ProductForm(),
            'product': Product.objects.all(),
            'year': getCurrentYear(),
        }
        return render(request, 'product.html', context)
    else:
        form = ProductForm(request.POST)
        if form.is_valid():
            mydata = form.save(commit=False)
            mydata.user_id = request.user.id
            mydata.save()
            messages.success(request, ('Register Edited Successfully'))
            return redirect('product')
        return render(request, 'product.html', {'form': form})


# @login_required(login_url='login')
# def productreturn(request, id):
#     data = Purchase.objects.get(pk=id)
#     form = ProductReturnForm(request.POST or None, instance=data)
#
#     if form.is_valid():
#         mydata = form.save(commit=False)
#         mydata.user_id = request.user.id
#         mydata.save()
#         return redirect('purchase')
#     context = {
#         'form': form,
#         'productreturn': Productreturn.objects.all(),
#         'year': getCurrentYear(),
#     }
#     return render(request, 'purchase.html', context)
#
#     # if request.method == 'GET':
#     #     #     context = {
#     #     #         'form': ProductReturnForm(),
#     #     #         'productreturn': Productreturn.objects.all(),
#     #     #         'year': getCurrentYear(),
#     #     #
#     #     #     }
#     #     #     return render(request, 'productreturn.html', context)
#     #     # else:
#     #     #     form = ProductReturnForm(request.POST)
#     #     #     if form.is_valid():
#     #     #         mydata = form.save(commit=False)
#     #     #         mydata.user_id = request.user.id
#     #     #         mydata.save()
#     #     #         return redirect('productreturn')
#     #     #     return render(request, 'productreturn.html', {'form': form})



@login_required(login_url='login')
def purchase(request,):
    if request.method == 'GET':
        context = {
            'form': PurchaseForm(),
            'purchase': Purchase.objects.all(),
        }
        return render(request, 'purchase.html', context, )
    else:
        form = PurchaseForm(request.POST)
        if form.is_valid():
            mydata = form.save(commit=False)
            mydata.user_id = request.user.id
            mydata.save()
            return redirect('purchase')
        return render(request, 'purchase.html', {'form': form})


@login_required(login_url='login')
def stock(request):
    if request.method == 'GET':
        context = {
            'form': StockForm(),
            'stock': Stock.objects.all(),
            'year': getCurrentYear(),
            'purchase': Purchase.objects.all(),

        }
        return render(request, 'stock.html', context)
    else:
        form = StockForm(request.POST)
        if form.is_valid():
            mydata = form.save(commit=False)
            # mydata.user_id = request.user.id
            mydata.save()
            return redirect('stock')
        return render(request, 'stock.html', {'form': form})


def getCurrentMonth():
    return datetime.date.today().month


def getCurrentYear():
    return datetime.date.today().year


def export_stock_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="stocks.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Stocks')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['quantity', 'sales', 'remaining', 'product_id', ]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = Stock.objects.all().values_list('quantity', 'sales', 'remaining', 'product_id', )
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response


def export_product_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="products.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Products')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['name', 'brand', 'total_price']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = Product.objects.all().values_list('name', 'brand', 'total_price')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response


def export_customer_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="customers.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Customers')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['name', 'contact', 'address']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = Customer.objects.all().values_list('name', 'contact', 'address')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response
