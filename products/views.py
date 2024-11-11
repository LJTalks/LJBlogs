# Standard library imports
from django.http import HttpResponse, HttpResponseRedirect

# Third-party imports
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import TemplateView

# Local application imports
from notes.models import Note
from products.models import Product, Purchase


# Products views
# def home(request):
#     return render(request, 'products/home.html')

def login_or_signup(request):
    """
    Custom view to show login or signup options when accessing paid products
    """
    next_url = request.GET.get(
        'next', '/')  # Get the next URL to redirect after login/signup
    return render(request, 'login_or_signup.html', {'next': next_url})

# Product List View for potential customers/all users


def product_list(request):
    # Fetch all products
    products = Product.objects.all().order_by('-publish_date')
    # Initialize the paginator, 6 products per page
    paginator = Paginator(products, 6)  # Show 6 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    # Pass the paginated object to the template
    return render(request, 'products/product_list.html', {'page_obj': page_obj})

# Product Detail View handles free for all, and purchased for logged in users


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    related_products = product.related_products.all()

    # Get the user's notes for this product if they are authenticated
    if request.user.is_authenticated:
        notes = Note.objects.filter(user=request.user, product=product)
    else:
        notes = None  # If not logged in, no notes available

    # Pass the notes to the context

    # Check purchased products for the current user
    if request.user.is_authenticated:
        purchased_products = Purchase.objects.filter(
            user=request.user).values_list('product_id', flat=True)
        related_products = related_products.exclude(id__in=purchased_products)
        # create purchased_retlated_products to store related products the user has purchased
        purchased_related_products = product.related_products.filter(
            id__in=purchased_products)
    else:
        # If the user is not authenticated,there will be no purchased products
        purchased_related_products = []

    # Initialise context with public content
    context = {
        'product': product,
        'notes': notes,  # Add user notes
        'related_products': related_products,
        # Add the purchased related products here
        'purchased_related_products': purchased_related_products,
        'is_purchased': False,  # Default to not purchased
    }

    # Check if the product is free for all users
    if product.price == 0.00:
        # If product is free, show full content to all users
        return render(request, 'products/product_detail.html', context)

    # If the product is not free, check user logged in and purchased
    if request.user.is_authenticated:
        has_purchased = Purchase.objects.filter(
            product=product, user=request.user, status=1).exists()

        if has_purchased:
            # User has purchased the product, show full content
            context['is_purchased'] = True
        else:
            # User hasn't purchased, show warning and redirect to purchase
            messages.warning(
                request, "You need to purchase this to access the full content.")
            return redirect('fake_payment', product_id=product.id)
    else:
        # If user is not logged in, direct to custom login/signup page,
        # then pass back to product
        messages.warning(request, "Please log in to access this product.")
        # Redirect to Django allauth login
        return redirect(f'/accounts/login/?next={request.path}')

    # Render the appropriate product detail view
    return render(request, 'products/product_detail.html', context)

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
                         f"Successfully purchased {product.title}!")

    # Redirect to purchase history
    return HttpResponseRedirect(reverse("purchase_history"))


# Purchase history
@login_required
def purchase_history(request):
    # Query for the logged-in user's purchases
    purchases = Purchase.objects.filter(
        user=request.user).order_by('-purchase_date')

    # Render the purchase history template with the purchase data
    return render(request, 'products/purchase_history.html', {'purchases': purchases})


# Fake payment view
@login_required
def fake_payment(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        # Simulate payment success and create a purchase
        Purchase.objects.create(
            product=product,
            user=request.user,
            quantity=1,  # Set default to 1 for simplicity
            price_paid=product.price,  # Use current product price
            status=1  # Mark as "completed"
        )
        # Add success message
        messages.add_message(request, messages.SUCCESS,
                             f'Successfully purchased {product.title}!')
        # Redirect to the purchase history page
        return redirect('purchase_history')
    # If not a POST request, render the fake payment page
    return render(request, 'products/fake_payment.html', {'product': product})


# Purchase success view
@login_required
def purchase_success(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'products/purchase_success.html', {'product': product})
