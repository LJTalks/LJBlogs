# Standard library imports
from django.http import HttpResponse, HttpResponseRedirect
# Third-party imports
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Exists, OuterRef, BooleanField, Value
from django.db import models
from django.db.models.functions import Coalesce
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import TemplateView
import stripe
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
# Local application imports
from notes.models import Note
from products.models import Product, Purchase
from django.views.decorators.http import require_POST
# For testing purposes, if CSRF token is not being passed
from django.views.decorators.csrf import csrf_exempt


def login_or_signup(request):
    """
    Custom view to show login or signup options when accessing paid products
    """
    next_url = request.GET.get(
        'next', '/')  # Get the next URL to redirect after login/signup
    return render(request, 'login_or_signup.html', {'next': next_url})


# Product List View for potential customers/all users
def product_list(request):
    # Fetch all products in development
    products = Product.objects.filter(status=1).order_by('-publish_date')
    if request.user.is_authenticated:
        purchases_subquery = Purchase.objects.filter(
            product_id=OuterRef('id'), user=request.user, status=1
        )
        products = products.annotate(
            is_purchased=Exists(purchases_subquery)
        )
    else:
        products = products.annotate(is_purchased=models.Value(False))
    # Initialize the paginator, 6 products per page
    paginator = Paginator(products, 6)  # Show 6 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    # Pass the paginated object to the template
    return render(
        request, 'products/product_list.html', {'page_obj': page_obj})


# Product Detail View handles free for all, and purchased for logged in users
#  Stripe payment
stripe.api_key = settings.STRIPE_SECRET_KEY


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    related_products = product.related_products.all()

    # Check if the user has already purchased the product
    is_purchased = False
    if request.user.is_authenticated:
        is_purchased = Purchase.objects.filter(
            product=product, user=request.user, status=1).exists()

    # Get user's notes for this product if they are authenticated
    notes = Note.objects.filter(
        user=request.user, product=product) if request.user.is_authenticated else None

    # Prepare context with all necessary variables
    context = {
        'product': product,
        'is_purchased': is_purchased,
        'notes': notes,
        'related_products': related_products,
        'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY,
    }

    # If the product is free or already purchased, show full content
    if product.price == 0.00 or is_purchased:
        return render(
            request, 'products/product_detail.html', context)

    # If the product is paid and not purchased, show the preview
    # with a "Purchase Now" button
    return render(request, 'products/product_detail.html', context)

    # Initialise context with public content
    context = {
        'product': product,
        'notes': notes,  # Add user notes
        'related_products': related_products,
        # Add the purchased related products here
        'purchased_related_products': purchased_related_products,
        'is_purchased': is_purchased,
        'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY,
    }

    # Check if the product is free for all users
    if product.price == 0.00 or is_purchased:
        # If product is free, show full content to all users
        return render(request, 'products/product_detail.html', context)

    if not request.user.is_authenticated:
        messages.warning(request, "Please log in to access this product.")
        return redirect(f'/accounts/login/?next={request.path}')

    return redirect('create_checkout_session', product_id=product.id)

    # # If the product is not free, check user logged in and purchased
    # if request.user.is_authenticated:
    #     has_purchased = Purchase.objects.filter(
    #         product=product, user=request.user, status=1).exists()

    #     if has_purchased:
    #         # User has purchased the product, show full content
    #         context['is_purchased'] = True
    #     else:
    #         # User hasn't purchased, show warning and redirect to purchase
    #         messages.warning(
    #             request, "You need to purchase this to access the full content.")
    #         return redirect('fake_payment', product_id=product.id)
    # else:
    #     # If user is not logged in, direct to custom login/signup page,
    #     # then pass back to product
    #     messages.warning(request, "Please log in to access this product.")
    #     # Redirect to Django allauth login
    #     return redirect(f'/accounts/login/?next={request.path}')

    # # Render the appropriate product detail view
    # return render(request, 'products/product_detail.html', context)

# View to handle product purchase (for customers)


@login_required  # Ensure the user is logged in before they can purchase
def purchase_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Quantity will be sent via POST form
    quantity_ordered = int(request.POST.get('quantity', 1))  # Default to one

    # Calculate the total price based on qty ordered
    total_price = quantity_ordered * product.price

    # Record the purchase in the Purchase model
    Purchase.objects.create(
        product=product,
        user=request.user,  # current logged in user
        quantity=quantity_ordered,
        price_paid=total_price,  # Use the current product price
        status=1  # Mark as "Completed"
    )

    # Add success message
    messages.add_message(request, messages.SUCCESS,
                         f"Thank you for purchasing {product.title}!")

    # Redirect to purchase history
    return HttpResponseRedirect(reverse("purchase_history"))


# Purchase history
@login_required
def purchase_history(request):
    # Query for the logged-in user's purchases
    purchases = Purchase.objects.filter(
        user=request.user).order_by('-purchase_date')

    # Render the purchase history template with the purchase data
    return render(
        request, 'products/purchase_history.html', {'purchases': purchases})


# # Fake payment view
# @login_required
# def fake_payment(request, product_id):
#     product = get_object_or_404(Product, id=product_id)

#     if request.method == 'POST':
#         # Simulate payment success and create a purchase
#         Purchase.objects.create(
#             product=product,
#             user=request.user,
#             quantity=1,  # Set default to 1 for simplicity
#             price_paid=product.price,  # Use current product price
#             status=1  # Mark as "completed"
#         )
#         # Add success message
#         messages.add_message(request, messages.SUCCESS,
#                              f'Successfully purchased {product.title}!')
#         # Redirect to the purchase history page
#         return redirect('purchase_history')
#     # If not a POST request, render the fake payment page
#     return render(request, 'products/fake_payment.html', {'product': product})


# Purchase success view
@login_required
def purchase_success(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    Purchase.objects.create(
        product=product,
        user=request.user,
        quantity=1,
        price_paid=product.price,
        status=1
    )
    messages.success(request, f'Successfully purchased {product.title}!')
    return redirect('purchase_history')

# @csrf_exempt
# def create_payment(request):
#     if request.method == "POST":
#         data = json.loads(request.body)
#         product_id = data.get("product_id")
#         product = Product.objects.get(id=product_id)

#         # Convert price to cents
#         # (Stripe requires amounts in the smallest currency unit)
#         amount = int(product.price * 100)

#         # Create a PaymentIntent with the price and currency
#         payment_intent = stripe.PaymentIntent.create(
#             amount=amount,
#             currency="gbp",
#         )

#         return JsonResponse({
#             'clientSecret': payment_intent['client_secret']
#         })


@csrf_exempt  # Use only for testing if necessary; ensure CSRF token is being passed in production
@require_POST  # Restrict to POST requests only
@login_required
def create_checkout_session(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'gbp',
                'product_data': {
                    'name': product.title,
                },
                # Convert to cents/pence
                'unit_amount': int(product.price * 100),
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=request.build_absolute_uri(
            reverse('purchase_success', args=[product.id])),
        cancel_url=request.build_absolute_uri(
            reverse('product_detail', args=[product.slug])),
    )
    return JsonResponse({'id': checkout_session.id})