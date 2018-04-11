from django.urls import path
from . import views

app_name = 'orders'
urlpatterns = [
    path('create/', views.order_create, name='order_create'),
    # path('detail/<int:order_id>/', views.order_detail, name='order_detail'),
    path('admin/order/<int:order_id>/', views.admin_order_detail, name='admin_order_detail'),
    path('admin/order/<int:order_id>/pdf/', views.admin_order_pdf, name='admin_order_pdf'),

    path('create_ajax/', views.OrderCreateAjaxView.as_view(), name='order_create_ajax'),
    path('checkout/', views.OrderCheckoutAjaxView.as_view(), name='order_checkout'),
    path('validation/', views.OrderImpAjaxView.as_view(), name='order_validation'),
    path('complete/', views.order_complete, name='order_complete'),
]