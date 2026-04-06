// Bookings functions
document.addEventListener('DOMContentLoaded', () => {
    const bookingForm = document.getElementById('bookingForm');
    
    if (bookingForm) {
        bookingForm.addEventListener('submit', handleBooking);
    }

    const token = localStorage.getItem('token');
    if (!token) {
        const bookingForm = document.getElementById('bookingForm');
        if (bookingForm) {
            bookingForm.style.display = 'none';
            document.querySelector('.booking-form-container').innerHTML += 
                '<p style="color: red;">Please <a href="login.html">login</a> to make a booking.</p>';
        }
    }

    loadUserBookings();
});

async function handleBooking(e) {
    e.preventDefault();

    const token = localStorage.getItem('token');
    if (!token) {
        showMessage('bookingMessage', 'Please login first', 'error');
        return;
    }

    const destination_id = document.getElementById('destination').value;
    const service_type = document.getElementById('service_type').value;
    const check_in = document.getElementById('check_in').value;
    const check_out = document.getElementById('check_out').value;
    const number_of_people = document.getElementById('people').value;

    try {
        const response = await fetch(`${API_BASE_URL}/bookings`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                destination_id: parseInt(destination_id),
                service_type: service_type,
                check_in_date: new Date(check_in).toISOString(),
                check_out_date: new Date(check_out).toISOString(),
                number_of_people: parseInt(number_of_people),
                total_price: 5000 // This should be calculated from service price
            })
        });

        const data = await response.json();

        if (response.ok) {
            showMessage('bookingMessage', 'Booking created successfully!', 'success');
            document.getElementById('bookingForm').reset();
            loadUserBookings();
        } else {
            showMessage('bookingMessage', data.detail || 'Booking failed', 'error');
        }
    } catch (error) {
        console.error('Booking error:', error);
        showMessage('bookingMessage', 'Error creating booking. Please try again.', 'error');
    }
}

async function loadUserBookings() {
    const token = localStorage.getItem('token');
    if (!token) return;

    try {
        const response = await fetch(`${API_BASE_URL}/bookings`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        const bookings = await response.json();
        const container = document.getElementById('userBookings');
        
        if (!container) return;

        if (bookings.length === 0) {
            container.innerHTML = '<p>No bookings yet. <a href="destinations.html">Book a tour now!</a></p>';
            return;
        }

        container.innerHTML = '';
        bookings.forEach(booking => {
            const item = document.createElement('div');
            item.className = 'booking-item';
            item.innerHTML = `
                <h3>Booking ID: ${booking.id}</h3>
                <p><strong>Destination:</strong> ${booking.destination_id}</p>
                <p><strong>Service:</strong> ${booking.service_type}</p>
                <p><strong>Check-in:</strong> ${new Date(booking.check_in_date).toLocaleDateString()}</p>
                <p><strong>Check-out:</strong> ${new Date(booking.check_out_date).toLocaleDateString()}</p>
                <p><strong>People:</strong> ${booking.number_of_people}</p>
                <p><strong>Total Price:</strong> ₹${booking.total_price}</p>
                <span class="booking-status status-${booking.status}">${booking.status.toUpperCase()}</span>
            `;
            container.appendChild(item);
        });
    } catch (error) {
        console.error('Error loading bookings:', error);
    }
}
