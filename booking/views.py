from django.shortcuts import render, get_object_or_404
# Import the BookingForm (Still need to create this)
from .forms import BookingForm
from .models import Booking  # Import the booking model

# Views for creating a new booking


def create_booking(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()  # Save the booking if the form is valid
            # Redirect to a success page (to be defined)
            return redirect('booking_success')
        else:
            form = BookingForm()  # on GET request, display an empty form

        return render(request, 'booking/create_booking.html', {'form': form})


def booking_success(request):
    return render(request, 'booking/booking_success.html')


def booking_list(request):
    bookings = Booking.objects.all()  # Get all bookings
    return render(request, 'booking/booking_list.html', {'bookings': bookings})


def booking_detail(request, booking_id):
    # Fetch the booking by ID
    booking = get_object_or_404(Booking, id=booking_id)
    return render(request, 'booking/booking_detail.html', {'booking': booking})
