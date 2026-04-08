// API Base URL
const API_BASE_URL = 'http://localhost:8000/api';
const CONTACT_PHONE = '+917607745628';
const CONTACT_WHATSAPP = '+917607745628';
const CONTACT_EMAIL = 'info@ayodhyaramnagari.com';

const priorityDestinationNames = ['Kashi', 'Vrindavan', 'Vidhyachal', 'Namshsiaryan'];
const fallbackDestinations = [
    {
        name: 'Kashi',
        short_description: 'Ancient holy city on the Ganges, famous for its evening aarti rituals.',
        rating: 4.9,
        image_url: 'https://content.skyscnr.com/m/26eaa06a2be696f0/original/GettyImages-525109131.jpg'
    },
    {
        name: 'Vrindavan',
        short_description: 'Divine town of Lord Krishna with beautiful temples and gardens.',
        rating: 4.8,
        image_url: 'https://www.makemytrip.com/tripideas/places/vrindavan'
    },
    {
        name: 'Vidhyachal',
        short_description: 'Historic spiritual retreat known for temples and scenic hills.',
        rating: 4.7,
        image_url: 'https://www.captureatrip.com/blog/vindhyachal-temple'
    },
    {
        name: 'Namshsiaryan',
        short_description: 'Discover a sacred pilgrimage site with rich spiritual traditions.',
        rating: 4.8,
        image_url: '/images/tree-place.svg'
    }
];

// Check if user is logged in
function checkAuthStatus() {
    const token = localStorage.getItem('token');
    const user = localStorage.getItem('user');
    const authButtons = document.getElementById('authButtons');
    const userProfile = document.getElementById('userProfile');

    if (token && user) {
        if (authButtons) authButtons.style.display = 'none';
        if (userProfile) userProfile.style.display = 'block';
    } else {
        if (authButtons) authButtons.style.display = 'block';
        if (userProfile) userProfile.style.display = 'none';
    }
}

// Logout function
function logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    checkAuthStatus();
    window.location.href = '../index.html';
}

function enhanceContactLinks() {
    document.querySelectorAll('p').forEach(p => {
        const text = p.textContent.trim();

        if (text.includes('📞 Phone: 7607745628')) {
            p.innerHTML = `📞 Phone: <a href="tel:${CONTACT_PHONE}">7607745628</a>`;
        }

        if (text.includes('💬 WhatsApp: 7607745628')) {
            p.innerHTML = `💬 WhatsApp: <a href="https://wa.me/${CONTACT_WHATSAPP.replace('+', '')}" target="_blank" rel="noopener">Chat on WhatsApp</a>`;
        }

        if (text.includes('📧 Email: info@ayodhyaramnagari.com')) {
            p.innerHTML = `📧 Email: <a href="mailto:${CONTACT_EMAIL}">${CONTACT_EMAIL}</a>`;
        }
    });
}

function normalizeDestinations(destinations) {
    const destinationMap = new Map(destinations.map(dest => [dest.name, dest]));
    const normalized = [];

    priorityDestinationNames.forEach(name => {
        if (destinationMap.has(name)) {
            normalized.push(destinationMap.get(name));
            destinationMap.delete(name);
        } else {
            const fallback = fallbackDestinations.find(item => item.name === name);
            if (fallback) normalized.push(fallback);
        }
    });

    destinationMap.forEach(dest => normalized.push(dest));
    return normalized;
}

// Load featured destinations
async function loadFeaturedDestinations() {
    try {
        const response = await fetch(`${API_BASE_URL}/destinations`);
        const destinations = await response.json();
        
        const container = document.getElementById('featuredDestinations');
        if (!container) return;

        const allDestinations = normalizeDestinations(destinations);
        container.innerHTML = '';
        allDestinations.slice(0, 3).forEach(dest => {
            const card = createDestinationCard(dest);
            container.appendChild(card);
        });
    } catch (error) {
        console.error('Error loading destinations:', error);

        const container = document.getElementById('featuredDestinations');
        if (!container) return;

        container.innerHTML = '';
        fallbackDestinations.slice(0, 3).forEach(dest => {
            const card = createDestinationCard(dest);
            container.appendChild(card);
        });
    }
}

// Create destination card element
function createDestinationCard(destination) {
    const card = document.createElement('div');
    card.className = 'destination-card';
    const rating = destination.rating || 4.7;
    const imageUrl = destination.image_url || '/images/tree-place.svg';
    const detailsUrl = destination.id ? `pages/destination-detail.html?id=${destination.id}` : 'pages/destinations.html';

    card.innerHTML = `
        <img class="destination-image" src="${imageUrl}" alt="${destination.name}" />
        <div class="destination-content">
            <h3>${destination.name}</h3>
            <p>${destination.short_description || 'Explore a beautiful pilgrimage destination.'}</p>
            <div class="destination-rating">
                <span class="stars">★★★★★ ${rating}</span>
            </div>
            <a href="${detailsUrl}" class="btn-primary">View Details</a>
        </div>
    `;
    return card;
}

// Load all destinations
async function loadAllDestinations() {
    try {
        const response = await fetch(`${API_BASE_URL}/destinations`);
        const destinations = await response.json();
        
        const container = document.getElementById('allDestinations');
        if (!container) return;

        const allDestinations = normalizeDestinations(destinations);
        container.innerHTML = '';
        allDestinations.forEach(dest => {
            const card = createDestinationCard(dest);
            container.appendChild(card);
        });
    } catch (error) {
        console.error('Error loading destinations:', error);

        const container = document.getElementById('allDestinations');
        if (!container) return;

        container.innerHTML = '';
        fallbackDestinations.forEach(dest => {
            const card = createDestinationCard(dest);
            container.appendChild(card);
        });
    }
}

// Load destinations dropdown for booking
async function loadDestinationsDropdown() {
    try {
        const response = await fetch(`${API_BASE_URL}/destinations`);
        const destinations = await response.json();
        
        const select = document.getElementById('destination');
        if (!select) return;

        destinations.forEach(dest => {
            const option = document.createElement('option');
            option.value = dest.id;
            option.textContent = dest.name;
            select.appendChild(option);
        });
    } catch (error) {
        console.error('Error loading destinations:', error);
    }
}

// Show message
function showMessage(elementId, message, type) {
    const element = document.getElementById(elementId);
    if (!element) return;

    element.textContent = message;
    element.className = type; // 'success' or 'error'
    element.style.display = 'block';
    
    setTimeout(() => {
        element.style.display = 'none';
    }, 5000);
}

// Initialize the page
document.addEventListener('DOMContentLoaded', () => {
    checkAuthStatus();
    enhanceContactLinks();
    
    if (document.getElementById('featuredDestinations')) {
        loadFeaturedDestinations();
    }
    
    if (document.getElementById('allDestinations')) {
        loadAllDestinations();
    }
    
    if (document.getElementById('destination')) {
        loadDestinationsDropdown();
    }
});
