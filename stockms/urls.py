from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', views.signup, name='signup'),
    path('', views.signin, name='login'),
    path('dashboard/', views.index, name='index'),
    path('logout/', views.my_logout, name='logout'),
    path('dashboard/customer',views.customer, name='customer'),
    path('dashboard/product', views.product, name='product'),
    path('dashboard/purchase', views.purchase, name='purchase'),
    path('dashboard/stock', views.stock, name='stock'),
    path('export/xls/', views.export_stock_xls, name='export_stock_xls'),
    path('export/product/', views.export_product_xls, name='export_product_xls'),
    path('export/customer/', views.export_customer_xls, name='export_customer_xls'),

]
