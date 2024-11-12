from django.urls import path, include
from . import views

# app_name = 'products'  # Namespace for clarity


urlpatterns = [
    path('all/', views.product_list, name='product_list'),  # Product list view
    path('<slug:slug>/', views.product_detail,
         name='product_detail'),  # Product summary view
    path('purchase/<int:product_id>/', views.purchase_product,
         name='purchase_product'),  # purchase product view
    path('history/', views.purchase_history,
         name='purchase_history'),  # Purchase history view
    path('accounts/', include('allauth.urls')),
    #     path('purchase/checkout/<int:product_id>/',
    #          views.checkout, name='cheeckout'),
    path('login_or_signup/', views.login_or_signup, name='login_or_signup'),
    #     path('purchase/checkout/<int:product_id>/',
    #          views.checkout, name='checkout'),
    path('purchase/success/<int:product_id>/',
         views.purchase_success, name='purchase_success'),
    #     path('create-payment/', views.create_payment, name='create_payment'),
    path('create-checkout-session/<int:product_id>/',
         views.create_checkout_session, name='create_checkout_session'),
]
