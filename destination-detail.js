// Destination Detail Page
document.addEventListener('DOMContentLoaded', async () => {
    const urlParams = new URLSearchParams(window.location.search);
    const destinationId = urlParams.get('id');

    if (!destinationId) {
        document.getElementById('destinationContent').innerHTML = '<p>Destination not found. <a href="destinations.html">Back to destinations</a></p>';
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/destinations/${destinationId}`);
        const destination = await response.json();

        // Load destination details
        const content = `
            <div class="destination-detail-header">
                <h1>${destination.name}</h1>
                <div class="destination-meta">
                    <span class="rating">★★★★★ ${destination.rating}</span>
                    <span class="reviews">${destination.reviews_count} reviews</span>
                </div>
            </div>

            <div class="destination-info">
                <div class="destination-image-large">
                    <div style="background: linear-gradient(135deg, var(--primary-color), var(--secondary-color)); 
                                width: 100%; height: 400px; display: flex; align-items: center; 
                                justify-content: center; font-size: 100px; border-radius: 10px;">
                        ${destination.name.charAt(0)}
                    </div>
                </div>

                <div class="destination-description">
                    <h2>About ${destination.name}</h2>
                    <p>${destination.description}</p>

                    <div class="destination-details-box">
                        <h3>Best Time to Visit</h3>
                        <p>${destination.best_time_to_visit || 'Year-round'}</p>
                    </div>

                    <div class="destination-details-box">
                        <h3>What to Expect</h3>
                        <ul>
                            <li>Sacred temples and pilgrimage sites</li>
                            <li>Ancient history and architecture</li>
                            <li>Spiritual experiences</li>
                            <li>Local culture and traditions</li>
                            <li>Comfortable accommodations</li>
                            <li>Guided tours and activities</li>
                        </ul>
                    </div>
                </div>
            </div>
        `;

        document.getElementById('destinationContent').innerHTML = content;

        // Load services
        loadServices(destinationId);

    } catch (error) {
        console.error('Error loading destination:', error);
        document.getElementById('destinationContent').innerHTML = '<p>Error loading destination. Please try again.</p>';
    }
});

async function loadServices(destinationId) {
    try {
        const response = await fetch(`${API_BASE_URL}/services/destination/${destinationId}`);
        const services = await response.json();

        const servicesGrid = document.getElementById('servicesGrid');
        servicesGrid.innerHTML = '';

        if (services.length === 0) {
            servicesGrid.innerHTML = '<p>No services available for this destination.</p>';
            return;
        }

        services.forEach(service => {
            const serviceCard = document.createElement('div');
            serviceCard.className = 'service-card';
            serviceCard.innerHTML = `
                <h3>${service.name}</h3>
                <p><strong>Type:</strong> ${service.service_type}</p>
                <p>${service.description}</p>
                <p class="price">₹${service.price_per_unit}/${service.unit}</p>
                <p class="contact">${service.contact_info || 'Contact for details'}</p>
                <button onclick="bookService(${service.id})" class="btn-primary">Book Now</button>
            `;
            servicesGrid.appendChild(serviceCard);
        });
    } catch (error) {
        console.error('Error loading services:', error);
    }
}

function bookService(serviceId) {
    const token = localStorage.getItem('token');
    if (!token) {
        window.location.href = 'login.html';
        return;
    }
    window.location.href = `bookings.html?serviceId=${serviceId}`;
}
