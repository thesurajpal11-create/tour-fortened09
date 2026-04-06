// Admin Dashboard Functions
let currentAdmin = null;

document.addEventListener('DOMContentLoaded', () => {
    checkAdminAccess();
    loadDashboard();
});

function checkAdminAccess() {
    const token = localStorage.getItem('token');
    const user = JSON.parse(localStorage.getItem('user') || '{}');

    if (!token || !user.is_admin) {
        alert('Admin access required!');
        window.location.href = '../index.html';
        return;
    }
    
    currentAdmin = user;
}

function switchSection(sectionId) {
    // Hide all sections
    document.querySelectorAll('.admin-section').forEach(section => {
        section.classList.remove('active');
    });

    // Remove active from all buttons
    document.querySelectorAll('.menuBtn').forEach(btn => {
        btn.classList.remove('active');
    });

    // Show selected section
    document.getElementById(sectionId).classList.add('active');

    // Mark button as active
    event.target.classList.add('active');

    // Load data based on section
    switch(sectionId) {
        case 'destinations':
            loadDestinations();
            break;
        case 'services':
            loadServices();
            break;
        case 'bookings':
            loadAllBookings();
            break;
        case 'users':
            loadUsers();
            break;
    }
}

async function loadDashboard() {
    const token = localStorage.getItem('token');

    try {
        // Load bookings for dashboard
        const bookingsResponse = await fetch(`${API_BASE_URL}/admin/bookings`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        const bookings = await bookingsResponse.json();

        // Calculate stats
        document.getElementById('totalBookings').textContent = bookings.length;
        document.getElementById('pendingBookings').textContent = 
            bookings.filter(b => b.status === 'pending').length;

        // Load destinations
        const destResponse = await fetch(`${API_BASE_URL}/destinations`);
        const destinations = await destResponse.json();
        document.getElementById('totalDestinations').textContent = destinations.length;

        // Display recent bookings
        displayRecentBookings(bookings.slice(0, 5));

    } catch (error) {
        console.error('Error loading dashboard:', error);
    }
}

async function loadDestinations() {
    try {
        const response = await fetch(`${API_BASE_URL}/destinations`);
        const destinations = await response.json();

        const tbody = document.querySelector('#destinationsTable tbody');
        tbody.innerHTML = '';

        destinations.forEach(dest => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${dest.id}</td>
                <td>${dest.name}</td>
                <td>${dest.short_description}</td>
                <td>${dest.rating}</td>
                <td>
                    <div class="action-buttons">
                        <button class="btn-small btn-edit" onclick="editDestination(${dest.id})">Edit</button>
                        <button class="btn-small btn-delete" onclick="deleteDestination(${dest.id})">Delete</button>
                    </div>
                </td>
            `;
            tbody.appendChild(row);
        });
    } catch (error) {
        console.error('Error loading destinations:', error);
    }
}

async function loadAllBookings() {
    const token = localStorage.getItem('token');

    try {
        const response = await fetch(`${API_BASE_URL}/admin/bookings`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        const bookings = await response.json();

        const tbody = document.querySelector('#bookingsTable tbody');
        tbody.innerHTML = '';

        bookings.forEach(booking => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${booking.id}</td>
                <td>${booking.user_id}</td>
                <td>${booking.destination_id}</td>
                <td>${booking.service_type}</td>
                <td>${new Date(booking.check_in_date).toLocaleDateString()}</td>
                <td>₹${booking.total_price}</td>
                <td><span class="status-badge status-${booking.status}">${booking.status}</span></td>
                <td>
                    <select onchange="updateBookingStatus(${booking.id}, this.value)">
                        <option value="pending" ${booking.status === 'pending' ? 'selected' : ''}>Pending</option>
                        <option value="confirmed" ${booking.status === 'confirmed' ? 'selected' : ''}>Confirmed</option>
                        <option value="completed" ${booking.status === 'completed' ? 'selected' : ''}>Completed</option>
                        <option value="cancelled" ${booking.status === 'cancelled' ? 'selected' : ''}>Cancelled</option>
                    </select>
                </td>
            `;
            tbody.appendChild(row);
        });
    } catch (error) {
        console.error('Error loading bookings:', error);
    }
}

function displayRecentBookings(bookings) {
    const tbody = document.querySelector('#recentBookingsTable tbody');
    tbody.innerHTML = '';

    bookings.forEach(booking => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${booking.id}</td>
            <td>${booking.user_id}</td>
            <td>${booking.destination_id}</td>
            <td>${booking.service_type}</td>
            <td>₹${booking.total_price}</td>
            <td><span class="status-badge status-${booking.status}">${booking.status}</span></td>
            <td>
                <select onchange="updateBookingStatus(${booking.id}, this.value)">
                    <option value="pending" ${booking.status === 'pending' ? 'selected' : ''}>Pending</option>
                    <option value="confirmed" ${booking.status === 'confirmed' ? 'selected' : ''}>Confirmed</option>
                    <option value="completed" ${booking.status === 'completed' ? 'selected' : ''}>Completed</option>
                    <option value="cancelled" ${booking.status === 'cancelled' ? 'selected' : ''}>Cancelled</option>
                </select>
            </td>
        `;
        tbody.appendChild(row);
    });
}

async function updateBookingStatus(bookingId, status) {
    const token = localStorage.getItem('token');

    try {
        const response = await fetch(`${API_BASE_URL}/admin/bookings/${bookingId}/status`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ status: status })
        });

        if (response.ok) {
            alert('Booking status updated successfully!');
        }
    } catch (error) {
        console.error('Error updating booking:', error);
    }
}

function showAddDestination() {
    document.getElementById('addDestinationForm').style.display = 
        document.getElementById('addDestinationForm').style.display === 'none' ? 'block' : 'none';
}

function showAddService() {
    document.getElementById('addServiceForm').style.display = 
        document.getElementById('addServiceForm').style.display === 'none' ? 'block' : 'none';
}

async function loadServices() {
    try {
        const response = await fetch(`${API_BASE_URL}/services`);
        const services = await response.json();

        const tbody = document.querySelector('#servicesTable tbody');
        tbody.innerHTML = '';

        services.forEach(service => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${service.id}</td>
                <td>${service.destination_id}</td>
                <td>${service.name}</td>
                <td>${service.service_type}</td>
                <td>₹${service.price_per_unit}</td>
                <td>
                    <button class="btn-small btn-delete" onclick="deleteService(${service.id})">Delete</button>
                </td>
            `;
            tbody.appendChild(row);
        });
    } catch (error) {
        console.error('Error loading services:', error);
    }
}

function loadUsers() {
    // Placeholder for user management
    alert('User management feature coming soon!');
}
