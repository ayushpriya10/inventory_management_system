from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.register, name='register'),
    path('logout', views.logout, name='logout'),
    path('login', views.login, name='login'),
    path('items', views.items, name='items-list'),
    path('orders', views.orders, name='orders-list'),
    path('vendors', views.vendors, name='vendor-list'),
    path('uploads', views.uploads, name='data-upload'),
    path('download-items', views.download_items, name='download-items'),
    path('download-vendors', views.download_vendors, name='download-vendors'),
    path('upload-vendors', views.upload_vendor, name='upload-vendors'),
    path('upload-items', views.upload_item, name='upload-items'),
    re_path(r'^order/(?P<id>OD\d+)$', views.order_detail_view, name='order-details'),
    re_path(r'^item/(?P<sku>[a-zA-Z]{3}\d{2})$', views.item_detail_view, name='item-details'),
    re_path(r'^vendor/(?P<ext>[a-zA-Z]{3})$', views.vendor_detail_view, name='vendor-details'),
    path('mail', views.send_email, name='send-mail'),
    re_path(r'^mailer/(?P<email>.+)$', views.mailer, name='mailer'),
    re_path(r'^process/(?P<id>OD\d+)$', views.process_order, name='process-order'),
    re_path(r'^confirm/(?P<id>OD\d+)$', views.confirm_order, name='confirm-order'),
    re_path(r'^cancel/(?P<id>OD\d+)$', views.cancel_order, name='cancel-order'),
]
