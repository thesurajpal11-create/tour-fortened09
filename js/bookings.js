// Booking request functions

document.addEventListener('DOMContentLoaded', () => {
    const bookingForm = document.getElementById('bookingForm');
    if (bookingForm) {
        bookingForm.addEventListener('submit', handleBooking);
    }
});

function handleBooking(e) {
    e.preventDefault();

    const fullName = document.getElementById('full_name').value.trim();
    const contactNumber = document.getElementById('contact_number').value.trim();
    const email = document.getElementById('email').value.trim();
    const pickupLocation = document.getElementById('pickup_location').value.trim();
    const dropLocation = document.getElementById('drop_location').value.trim();
    const startDate = document.getElementById('start_date').value;
    const packageType = document.getElementById('package_type').value;
    const hotelRating = document.getElementById('hotel_rating').value;
    const roomType = document.getElementById('room_type').value;
    const cabType = document.getElementById('cab_type').value;
    const karmakandService = document.getElementById('karmakand_service').value;

    if (!fullName || !contactNumber || !email || !pickupLocation || !dropLocation || !startDate || !packageType || !hotelRating || !roomType || !cabType || !karmakandService) {
        showMessage('bookingMessage', 'Please fill in all required booking fields.', 'error');
        return;
    }

    const bookingDetails = {
        fullName,
        contactNumber,
        email,
        pickupLocation,
        dropLocation,
        startDate,
        packageType,
        hotelRating,
        roomType,
        cabType,
        karmakandService
    };

    console.log('Booking request submitted:', bookingDetails);
    showMessage('bookingMessage', 'Your booking request has been submitted. We will contact you shortly at ' + email + '.', 'success');
    document.getElementById('bookingForm').reset();
}

function showMessage(elementId, message, type) {
    const element = document.getElementById(elementId);
    if (!element) return;

    element.textContent = message;
    element.className = type;
    element.style.display = 'block';

    setTimeout(() => {
        element.style.display = 'none';
    }, 6000);
}
