from django.urls import path, include
from . import views

urlpatterns = [
    path('all/', views.product_list, name='product_list'),  # Product list view
    path('accounts/', include('allauth.urls')),
    path('products/<slug:slug>/', views.product_detail,
         name='product_detail'),  # Product summary view
    path('purchase/<int:product_id>/', views.purchase_product,
         name='purchase_product'),  # purchase product view
    path('history/', views.purchase_history,
         name='purchase_history'),  # Purchase history view
    path('purchase/fake_payment/<int:product_id>/',
         views.fake_payment, name='fake_payment'),
    path('login_or_signup/', views.login_or_signup, name='login_or_signup'),
]
