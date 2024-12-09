# Standard library imports
from django.http import (
    HttpResponse,
    HttpResponseRedirect,
    HttpResponseForbidden,
    HttpResponseBadRequest
)
# Third-party imports
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Exists, OuterRef, Q, Value
from django.db import models
from django.db.models.functions import Coalesce
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import TemplateView
import stripe
from django.conf import settings
from django.http import JsonResponse
# Local application imports
from notes.models import Note
from products.models import Product, Purchase
from django.views.decorators.http import require_POST
from django.views import generic
from django.template.loader import render_to_string
import os

# # For testing purposes, if CSRF token is not being passed
# from django.views.decorators.csrf import csrf_exempt


def login_or_signup(request):
    """
    Custom view to show login or signup options when accessing paid products
    """
    next_url = request.GET.get(
        'next', '/')  # Get the next URL to redirect after login/signup
    return render(request, 'login_or_signup.html', {'next': next_url})


# Product List View for potential customers/all users
class ProductListView(generic.ListView):
    model = Product
    template_name = "products/product_list.html"
    paginate_by = 6

    def get_queryset(self):
        queryset = super().get_queryset().order_by("-publish_date")

        if os.path.exists('env.py'):
            queryset = queryset.filter(Q(status=1) | Q(status=0))
        else:
            queryset = queryset.filter(status=1)

        # Annotate purchase status if user is authenticated
        if self.request.user.is_authenticated:
            purchases_subquery = Purchase.objects.filter(
                product_id=OuterRef('id'), user=self.request.user, status=1
            )
            queryset = queryset.annotate(
                is_purchased=Exists(purchases_subquery))
        else:
            queryset = queryset.annotate(is_purchased=Value(False))

        return queryset

    def render_to_response(self, context, **response_kwargs):
        # Handle AJAX requests for dynamic loading or searching
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            query = self.request.GET.get("q", "")
            products = context['object_list']
            products_html = render_to_string(
                'products/partials/product_list_partial.html', {
                    'products': products}
            )
            if products.exists():
                message = ""
            else:
                message = f'No results found for "{query}"'

            return JsonResponse(
                {'products_html': products_html, 'message': message})

        return super().render_to_response(context, **response_kwargs)


# Product Detail View handles free for all, and purchased for logged in users
#  Stripe payment
stripe.api_key = settings.STRIPE_SECRET_KEY


# If error it's in here; changing view logic from free or paid, to category inc free or paid.
def product_detail(request, slug):
    # Fetch the product (include drafts in development)
    if os.path.exists('env.py'):
        product = get_object_or_404(Product.objects.filter(
            Q(status=1) | Q(status=0)), slug=slug)
        related_products = product.related_products.all()
    else:
        product = get_object_or_404(
            Product.objects.filter(status=1), slug=slug)
        related_products = product.related_products.filter(status=1)

    # Check if the user has already purchased the product
    is_purchased = request.user.is_authenticated and Purchase.objects.filter(
        product=product, user=request.user, status=1).exists()

    # Debug category
    print(f"Product category: {product.category}")

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

    # Email-required products need login
    if product.category == 'email required' and not request.user.is_authenticated:
        messages.info(
            request, "Please log in or create an account to access this product."
        )
        return redirect(f'/accounts/login/?next={request.path}')

    if product.price == 0.00 or is_purchased:
        # Free or purchased product: show full content
        context = {
            'product': product,
            'show_full_content': True,
            'notes': notes,
            'related_products': related_products,
        }
    else:
        # Paid but not purchased: show preview and Buy Now button
        context = {
            'product': product,
            'show_full_content': False,
            'show_buy_now': True,
            'notes': notes,
            'related_products': related_products,
            'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY,
        }

    # Render the appropriate template
    return render(request, 'products/product_detail.html', context)

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


# @csrf_exempt  # Use only for testing if necessary; ensure CSRF token is being passed in production
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
